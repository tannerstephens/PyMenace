from PyQt4 import QtGui, QtCore
from menace.ui import menaceDesign
import menace.menace as menace
import sys, os

class Menace(QtGui.QMainWindow, menaceDesign.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.menace = menace.Menace(10)
        self.connectFunctions()
        win = self.menace.play()
        self.update()
        self.setWindowIcon(QtGui.QIcon("./menace/ui/corner.png"))
        if os.path.isfile("./menace/learning.dat"):
            self.menace.load("./menace/learning.dat")

    def update(self):
        # Update buttons with current board state
        # Disable already used buttons
        self.UL.setText(self.menace.board[0])
        self.ML.setText(self.menace.board[3])
        self.LL.setText(self.menace.board[6])
        self.UM.setText(self.menace.board[1])
        self.MM.setText(self.menace.board[4])
        self.LM.setText(self.menace.board[7])
        self.UR.setText(self.menace.board[2])
        self.MR.setText(self.menace.board[5])
        self.LR.setText(self.menace.board[8])
        self.UL.setEnabled(self.menace.board[0]==" ")
        self.ML.setEnabled(self.menace.board[3]==" ")
        self.LL.setEnabled(self.menace.board[6]==" ")
        self.UM.setEnabled(self.menace.board[1]==" ")
        self.MM.setEnabled(self.menace.board[4]==" ")
        self.LM.setEnabled(self.menace.board[7]==" ")
        self.UR.setEnabled(self.menace.board[2]==" ")
        self.MR.setEnabled(self.menace.board[5]==" ")
        self.LR.setEnabled(self.menace.board[8]==" ")

    def closeEvent(self, event):
        # Save the learned data on close
        self.menace.save("./menace/learning.dat")
        event.accept()

    def connectFunctions(self):
        # Connect the button events to the correct functions
        self.UL.clicked.connect(self.ul_button)
        self.ML.clicked.connect(self.ml_button)
        self.LL.clicked.connect(self.ll_button)
        self.UM.clicked.connect(self.um_button)
        self.MM.clicked.connect(self.mm_button)
        self.LM.clicked.connect(self.lm_button)
        self.UR.clicked.connect(self.ur_button)
        self.MR.clicked.connect(self.mr_button)
        self.LR.clicked.connect(self.lr_button)


    # xx_button all are functionally the same, just corresponding to different
    # board positions.
    def ul_button(self):
        # Play in position
        # 012
        # 345
        # 678
        win = self.menace.play(0)
        self.update()

        if win:
            # If win detected, learn from moves
            self.menace.learn()
            # Menace takes next turn outside of if
            self.update()

        # Take computer turn
        win = self.menace.play()
        self.update()
        if win:
            # If win detected, learn from moves
            self.menace.learn()
            # Menace won, needs another turn
            self.menace.play()
            self.update()

    def ml_button(self):
        win = self.menace.play(3)
        self.update()
        if win:

            self.menace.learn()
            self.update()

        win = self.menace.play()
        self.update()
        if win:

            self.menace.learn()
            self.menace.play()
            self.update()


    def ll_button(self):
        win = self.menace.play(6)
        self.update()
        if win:

            self.menace.learn()
            self.update()

        win = self.menace.play()
        self.update()
        if win:

            self.menace.learn()
            self.menace.play()
            self.update()


    def um_button(self):
        win = self.menace.play(1)
        self.update()
        if win:

            self.menace.learn()
            self.update()

        win = self.menace.play()
        self.update()
        if win:

            self.menace.learn()
            self.menace.play()
            self.update()


    def mm_button(self):
        win = self.menace.play(4)
        self.update()
        if win:

            self.menace.learn()
            self.update()

        win = self.menace.play()
        self.update()
        if win:

            self.menace.learn()
            self.menace.play()
            self.update()


    def lm_button(self):
        win = self.menace.play(7)
        self.update()
        if win:

            self.menace.learn()
            self.update()

        win = self.menace.play()
        self.update()
        if win:

            self.menace.learn()
            self.menace.play()
            self.update()


    def ur_button(self):
        win = self.menace.play(2)
        self.update()
        if win:

            self.menace.learn()
            self.update()

        win = self.menace.play()
        self.update()
        if win:

            self.menace.learn()
            self.menace.play()
            self.update()


    def mr_button(self):
        win = self.menace.play(5)
        self.update()
        if win:

            self.menace.learn()
            self.update()

        win = self.menace.play()
        self.update()
        if win:

            self.menace.learn()
            self.menace.play()
            self.update()


    def lr_button(self):
        win = self.menace.play(8)
        self.update()
        if win:

            self.menace.learn()
            self.update()

        win = self.menace.play()
        self.update()
        if win:

            self.menace.learn()
            self.menace.play()
            self.update()



def run():
    app = QtGui.QApplication(sys.argv)
    men = Menace()
    men.show()
    return app.exec_()