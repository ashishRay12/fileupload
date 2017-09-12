from main import app
from .views import Register, Authenticate, UploadFiles, QueryFiles

app.add_route('/register', Register())
app.add_route('/authenticate', Authenticate())
app.add_route('/upload', UploadFiles())
app.add_route('/query', QueryFiles())
