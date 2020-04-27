import json


class GetResults():
    all_data = {}
    all_data['covid'] = []
    all_data['general'] = []
    all_data['words'] = {}
    temp_list = []

    def __init__(self):
        self.all_data = {}
        self.all_data['covid'] = []
        self.all_data['general'] = []
        self.all_data['words'] = {}
        self.temp_list = []

    @classmethod
    def get_general_news(self, parsed_items):
        self.all_data['general'].append(parsed_items)

    @classmethod
    def get_covid_news(self, parsed_items):
        self.all_data['covid'].append(parsed_items)

    @classmethod
    def dump_json(self):
        # print(self.all_data)
        with open('latest.json', 'w') as latest_file:
            json.dump(self.all_data, latest_file, indent=4, sort_keys=True)
            latest_file.close()

    @classmethod
    def append_temp(self, parsed):
        self.temp_list.append(parsed)

    @classmethod
    def count_words(self):
        try:
            with open('latest.json', 'r') as json_file:
                existing_words = json.load(json_file)
                for sentence in self.temp_list:
                    for new_word in sentence:
                        # if new_word in self.all_data['words']:
                        if new_word in existing_words['words']:
                            # add_count = self.all_data['words'][new_word] + 1
                            add_count = existing_words['words'][new_word] + 1
                            self.all_data['words'][new_word] = add_count
                        else:
                            self.all_data['words'][new_word] = 1
                print(self.all_data['words'])
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            print("First scrape for today. Have a nice day! ;)")
            for sentence in self.temp_list:
                for new_word in sentence:
                    if new_word in self.all_data['words']:
                        add_count = self.all_data['words'][new_word] + 1
                        self.all_data['words'][new_word] = add_count
                    else:
                        self.all_data['words'][new_word] = 1
