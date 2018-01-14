FROM ubuntu:16.04

RUN apt-get update \
	&& apt-get install -y python python-pip build-essential libssl-dev libffi-dev python-dev \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install ansible \
	&& pip install flask \
	&& pip install requests

# add application
COPY ./application/ /var/www/

# add ansible config and ssh private key
COPY ./ansible.cfg /etc/ansible/ansible.cfg
COPY ./id_rsa /etc/ssh/id_rsa_ansible
RUN chmod 400 /etc/ssh/id_rsa_ansible

EXPOSE 80
CMD /var/www/application.py