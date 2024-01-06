import sys
sys.path.append("/root")
from Navigation.Navigation import Navigation

if __name__ == "__main__":
    navigation = Navigation()
    navigation.init_navigation()
