from binaries.Updater import Updater
# start by update if needed
update = Updater()
update.start()

from binaries.Requierements import install_requierement
# install requierment if not already installed
install_requierement()

from binaries.Kernel import Kernel
# ========================================== FIN DES IMPORTS ========================================================= #



if __name__ == '__main__':
    try:
        kernel = Kernel()
        kernel.start()
    except KeyboardInterrupt:
        kernel._action_before_stopping_server()
        print("Exiting")

