import sys
sys.path.append("/root")
from Navigation.Navigation import Navigation

#start application
if __name__ == "__main__":
    navigation = Navigation()
    navigation.init_navigation()
