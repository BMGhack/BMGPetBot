import os, sys
PROJECT_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.pardir)
sys.path.append(PROJECT_ROOT)

from fetchers.petfetcher import get_petfinder_pet


if __name__ == '__main__':
	print(get_petfinder_pet("47401"))
	print(get_petfinder_pet("47401",pick_random=True))
