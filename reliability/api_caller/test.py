from api_call import ApiCall


if __name__ == "__main__":
    ac = ApiCall('http://192.168.99.100')
    ac.make_vote()
