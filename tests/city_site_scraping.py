"""

Scrapin' test

"""

import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from fetchers.petfetcher import get_city_website_pet
if __name__ == '__main__':
	print(get_city_website_pet(True))