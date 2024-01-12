FROM python:3.12.1-slim-bullseye

# Set the timezone
ENV TZ=America/Los_Angeles
RUN apt-get update && apt-get install -y \
    bash \
    npm \
    yarn \
    vim \
    curl \
    tzdata \
    git \
    gcc \
    # software-properties-common \
    zip \
    sudo \
    unixodbc-dev \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

#Download appropriate package for the OS version
#Choose only ONE of the following, corresponding to your OS version

# #Debian 9
# RUN curl https://packages.microsoft.com/config/debian/9/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# #Debian 10
# RUN curl https://packages.microsoft.com/config/debian/10/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

# #Debian 11
RUN curl https://packages.microsoft.com/config/debian/11/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

#Debian 12
# RUN curl https://packages.microsoft.com/config/debian/12/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

ENV ACCEPT_EULA=Y 

RUN apt-get update  && apt-get install -y \
    msodbcsql18 \
# optional: for bcp and sqlcmd
    mssql-tools18 
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
# RUN source ~/.bashrc
RUN . ~/.bashrc
# optional: for unixODBC development headers
RUN apt-get install -y unixodbc-dev libgssapi-krb5-2
# optional: kerberos library for debian-slim distributions


WORKDIR /opt/app

COPY . .

RUN pip install --no-cache-dir -r requirements-prod.txt

EXPOSE 5001
ENV FLASK_DEBUG=1
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
