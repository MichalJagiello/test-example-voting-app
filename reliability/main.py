import random
import time

from api_caller.api_call import ApiCall
from config.config import Config
from container_managment.manager import ContainerManager
from scrapper.scrapper import Scrapper
from splash_client.client import SplashClient


class ReliabilityTest(object):
    """docstring for ReliabilityTest."""
    def __init__(self, config_path=None):
        self.config = Config(config_path)

        self.microservices_api_call = ApiCall(
            self.config['MICROSERVICES_VOTE_URL']
        )
        self.monolith_api_call = ApiCall(
            self.config['MONOLITH_VOTE_URL']
        )

        self.microservices_container_manager = ContainerManager(
            self.config['MICROSERVICES_DOCKER_HOST'],
            self.config['MICROSERVICES_DOCKER_CERT_PATH']
        )
        self.monolith_container_manager = ContainerManager(
            self.config['MONOLITH_DOCKER_HOST'],
            self.config['MONOLITH_DOCKER_CERT_PATH']
        )

        self.splash_client = SplashClient(self.config['SPLASH_SERVER_URL'])

        self._db_off = False

        self._get_start_tests_votes()

        self.number_of_requests = random.randint(100, 1000)
        self.number_of_requests_without_db = random.randint(10, 99)
        # self.number_of_requests = 10
        # self.number_of_requests_without_db = 5
        self.turn_off_db_request_number = int((self.number_of_requests -
                                               self.number_of_requests_without_db) / 2)

        print("### TESTS START ###")
        print("Number of requests: {}".format(self.number_of_requests))
        print("Number of requests with db turned off: {}".format(
            self.number_of_requests_without_db)
        )
        for request_number in range(self.number_of_requests):
            if request_number == self.turn_off_db_request_number:
                print("Turn off db")
                self._turn_off_db()
            self.microservices_api_call.make_vote()
            self.monolith_api_call.make_vote()
            if self._db_off:
                self.number_of_requests_without_db -= 1
                if self.number_of_requests_without_db == 0:
                    print("Turn on db")
                    self._turn_on_db()

        self._get_end_tests_votes()

        print("### TESTS RESULTS ###")
        print("Lost {} votes in microservices app".format(self.number_of_requests -
                                                          (self.end_microservices_votes -
                                                           self.start_microservices_votes)))
        print("Lost {} votes in monolith app".format(self.number_of_requests -
                                                     (self.end_monolith_votes -
                                                      self.start_monolith_votes)))

    def _get_tests_votes(self):
        microservices = Scrapper.get_votes(
            self.splash_client.render_html(
                self.config['MICROSERVICES_RESULTS_URL']
            )
        )
        monolith = Scrapper.get_votes(
            self.splash_client.render_html(
                self.config['MONOLITH_RESULTS_URL']
            )
        )
        return microservices, monolith

    def _get_start_tests_votes(self):
        self.start_microservices_votes, self.start_monolith_votes = self._get_tests_votes()

    def _get_end_tests_votes(self):
        self.end_microservices_votes, self.end_monolith_votes = self._get_tests_votes()

    def _turn_off_db(self):
        self._turn_off_microservices_db()
        self._turn_off_monolith_db()
        self._db_off = True

    def _turn_on_db(self):
        self._turn_on_microservices_db()
        self._turn_on_monolith_db()
        self._db_off = False
        time.sleep(1)

    def _turn_off_microservices_db(self):
        db = self.microservices_container_manager.get_container(
            self.config['MICROSERVICES_DB_CONTAINER_NAME']
        )
        db.stop()

    def _turn_off_monolith_db(self):
        db = self.monolith_container_manager.get_container(
            self.config['MONOLITH_DB_CONTAINER_NAME']
        )
        db.stop()

    def _turn_on_microservices_db(self):
        db = self.microservices_container_manager.get_container(
            self.config['MICROSERVICES_DB_CONTAINER_NAME']
        )
        db.start()

    def _turn_on_monolith_db(self):
        db = self.monolith_container_manager.get_container(
            self.config['MONOLITH_DB_CONTAINER_NAME']
        )
        db.start()


if __name__ == "__main__":
    rt = ReliabilityTest()
