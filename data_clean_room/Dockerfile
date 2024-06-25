FROM python:3.9-slim

RUN apt update && apt install -y vim git gnupg && \
    pip install pandas numpy jupyterlab && \
    jupyter lab --generate-config && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
