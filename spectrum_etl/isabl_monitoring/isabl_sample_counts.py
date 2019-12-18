import isabl_cli
import os


os.environ["ISABL_API_URL"] = 'https://isabl.shahlab.ca/api/v1/'
os.environ["ISABL_CLIENT_ID"] = "1"


samples_dict = {}
samples = isabl_cli.get_instances('samples')
samples_dict["total_samples"] = len(samples)
print(samples_dict)


# if elasticsearch index does not exist, create one and add mapping


# if record does not exist create record for sample count


# if record exists then update value of record