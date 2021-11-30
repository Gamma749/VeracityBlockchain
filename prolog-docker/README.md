# Jupyter-Prolog-Docker

The aim of this part of the directory is to get a jupyter notebook running in a docker container with prolog functionality. Each of these steps will be taken one at a time.

## Running this project
- Pull the Docker image: `docker pull gamma749/deepnote-swipl`
    - Alternatively, build the image yourself using the provided dockerfile. If renaming the image, please ensure your also rename the image called on in `create-container.sh`
    - If building yourself, pull the submodule jupyter-swi-prolog (or [clone from here](https://github.com/veracitylab/jupyter-swi-prolog)). Ensure that the submodule and requirements.txt are in a `setup` directory. Run `pip install -r ./requirements.txt` from withing the container to ensure the kernel installed correctly.
- Run `./create-container.sh` to destroy the previous container (if any) and start a new container, running jupyter notebook
- Once jupyter starts, it will print a link to the terminal. Cmd+click (or copy paste) to follow this link in your host browser.
- To use magic file consultation, start a cell of prolog with `%file: <name>.pl`.

## Configuration
Note that your notebooks are kept in the `notebooks` directory. This is for persistent storage of the notebooks outside of the docker container. To change where your notebooks are kept, change the volume mount in `create-container` from `-v $(pwd)/notebooks:/notebooks` to `-v {YOUR_DIR_HERE}:/notebooks`

The SWIPL kernel for jupyter and all magic file scripting is kept in the `setup/jupyter-swi-prolog` directory. If you want to make further changes to the kernel, do so here so the changes are persistent. The kernel is taken from [this project](https://github.com/veracitylab/jupyter-swi-prolog)
