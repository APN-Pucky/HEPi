FROM apnpucky/gentoo-hepi

RUN lhapdf install cteq6l1 cteq66 CT14lo CT14nlo

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}

RUN useradd --shell /bin/bash --comment "Default user" --non-unique --uid ${NB_UID} ${NB_USER}

# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}
WORKDIR ${HOME}
USER ${NB_USER}
ENV PATH "$PATH:${HOME}/.local/bin"

RUN python3 -m pip install --no-cache-dir --break-system-packages notebook jupyterlab jupyterhub hepi==0.2.17
