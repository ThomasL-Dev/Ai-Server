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
    except Exception as e:
        from binaries.Logger import Logger
        import traceback
        Logger().error("{} : {}".format(str(e), str(traceback.print_exc())))
