from flask import render_template

class ConafeException(Exception):
    def __init__(self, code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code

    def response(self):
        return render_template('error.html', description=str(self), code=self.code), self.code