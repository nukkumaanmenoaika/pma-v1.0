from os import listdir
from asyncio import run, gather, create_task
from pandas import read_csv, DataFrame
from json import dumps

class Loader:
    __file_path = "csv/"
    __list_files = listdir(__file_path)

    __id_database_var = {}
    __id_database_file = "id_database.txt"

    @classmethod
    async def read_all_database_for_init_id_database(cls, i: str):
        return (i, list(set(DataFrame(read_csv(cls.__file_path + i, delimiter=';', dtype=str))["PATIENTID"])))

    @classmethod
    async def load_all_database(cls):
        time_result = []
        for i in cls.__list_files: time_result.append(create_task(cls.read_all_database_for_init_id_database(i)))
        final_result = await gather(*time_result)
        return final_result

    @classmethod
    async def save_single(cls, obj):
        cls.__id_database_var.update({obj[0]: obj[1]})


    @classmethod
    async def save_id_database(cls, obj):
        time_result = []
        for i in obj: time_result.append(create_task(cls.save_single(i)))
        await gather(*time_result)
        with open(cls.__id_database_file, "w") as file: file.write(dumps(cls.__id_database_var))


    def __new__(cls, *args, **kwargs):
        run(cls.save_id_database(run(cls.load_all_database())))

Loader()
