FROM python:3.7
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
CMD streamlit run streamlit_app.py --server.port $PORT