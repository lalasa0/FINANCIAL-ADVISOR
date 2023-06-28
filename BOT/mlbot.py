import constants
import sys
import openai
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import(
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QTextEdit
)
openai.api_key = constants.API_KEY

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.logo_label = QLabel()
        self.logo_pixmap = QPixmap('B.jpg').scaled(150,150, Qt.KeepAspectRatio , Qt.SmoothTransformation)
        self.logo_label.setPixmap(self.logo_pixmap)
        self.input_label = QLabel('Ask a Question:')
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Type here..')
        self.answer_label = QLabel('Answer:')
        self.answer_field = QTextEdit()
        self.answer_field.setReadOnly(True)
        self.submit_button = QPushButton('Submit')
        self.submit_button.setStyleSheet (

            '''
                QPushButton {
                    background-color: #0000FF;
                    border: none;
                    color:skyblue;
                    padding: 15px 32px;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius:10px;
                    }
                QPushButton:hover{
                background-color: #000080;        
                }  
                    '''    
        )
        self.popular_questions_group =QGroupBox('Popular Questions')
        self.popular_questions_layout = QVBoxLayout()
        self.popular_questions = ['How can I improve my credit score?','What are the best investment options for beginners?','How can I start investing in the stock market?']
        self.question_buttons = []

        layout = QVBoxLayout()
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.logo_label,alignment=Qt.AlignCenter)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.submit_button)
        layout.addLayout(input_layout)

        layout.addWidget(self.answer_label)
        layout.addWidget(self.answer_field)

        for question in self.popular_questions:
            button = QPushButton(question)
            button.setStyleSheet(
                '''
                QPushButton {
                background-color:#0000FF
                border: 2px solid #FFFFFF;
                color:skyblue;
                padding: 10px 20px;
                font-size: 18px;
                font-weight: bold;
                border-radius:5px; 
                }
                QPushButton:hover{
                    background-color:#000080
                    color:sky blue    
                }
                '''
            )
            button.clicked.connect(lambda _, q=question: self.input_field.setText(q))
            self.popular_questions_layout.addWidget(button)
            self.question_buttons.append(button)
        self.popular_questions_group.setLayout(self.popular_questions_layout)
        layout.addWidget(self.popular_questions_group)

        self.setLayout(layout)

        self.setWindowTitle('Personal Finance Advise Bot')
        self.setGeometry(200,200,600,600)

        self.submit_button.clicked.connect(self.get_answer)
    def get_answer(self):
        question = self.input_field.text()

        completion = openai.ChatCompletion.create(
            model= "gpt-3.5-turbo-0301",
            messages = [{"role": "user","content": "You are a Personal Finance Advisor. Answer the following question in a concise way or with bullet points. "},
                        {"role": "user" , "content":f'{question}'}],
            max_tokens = 1024,
            n = 1,
            stop = None,
            temperature = 0.7
        )

        answer = completion.choices[0].message.content

        self.answer_field.setText(answer)
if __name__ == '__main__':
    app =QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())