from functools import cache
from os import listdir
from subprocess import call
from asyncio import gather, create_task
from pandas import DataFrame, read_csv, options
from json import loads
from os.path import getsize

class Database:

    __file_path = "csv/"
    __list_files = listdir(__file_path)
    __loader_file = call(["python.exe", "loader.py"])
    __size_files = None
    __id_database_var = {}
    __id_database_file = "id_database.txt"


    def __new__(cls, *args, **kwargs):
        with open(cls.__id_database_file, "r") as file:
            cls.__id_database_var = loads(file.read())
        return super().__new__(cls)


    @classmethod
    async def __size(cls, i):
        return getsize(cls.__file_path + i)

    @classmethod
    async def get_min_size_file(cls):
        time_result = []
        for i in cls.__list_files: time_result.append(create_task(cls.__size(i)))
        cls.__size_files = list(await gather(*time_result))
        min_size = min(cls.__size_files)
        return cls.__list_files[cls.__size_files.index(min_size)]
    @cache
    async def __check_id(self, patient_id, patient_list):
        if patient_id in patient_list: return True
        else: return False

    @cache
    async def write_database(self,  PATIENTID = None, BIRTHDATE = None, SEX = None,  SHEDULEDATE = None, TYPE = None, EXAMID = None, MKBCODE= None):
        time_result = []
        for i in self.__id_database_var.values(): time_result.append(create_task(self.__check_id(PATIENTID, tuple(i))))
        result = await gather(*time_result)
        if any(result):
            with open(self.__file_path + self.__list_files[result.index(True)], mode="a") as file:
                DataFrame(
                    {"PATIENTID": [PATIENTID], "BIRTHDATE": [BIRTHDATE], "SEX": [SEX], "SHEDULEDATE": [SHEDULEDATE], "EXAMID": [EXAMID],
                     "TYPE": [TYPE], "MKBCODE": [MKBCODE]}).to_csv(file, sep=";", index=False, header=False)
        else:
            with open(await self.get_min_size_file(), mode="a") as file:
                DataFrame(
                    {"PATIENTID": [PATIENTID], "BIRTHDATE": [BIRTHDATE], "SEX": [SEX], "SHEDULEDATE": [SHEDULEDATE],
                     "TYPE": [TYPE], "EXAMID": [EXAMID], "MKBCODE": [MKBCODE]}).to_csv(file, sep=";", index=False,
                                                                   header=False)
    @cache
    async def __find_patient(self, var, patient_id):
        if patient_id in var: return True
        else: return False

    @cache
    async def read_patients(self, patient_id):
        time_result = []
        for i in self.__id_database_var.values(): time_result.append(create_task(self.__find_patient(tuple(i), patient_id)))
        result = await gather(*time_result)
        if any(result):
            df = DataFrame(read_csv(self.__file_path + self.__list_files[result.index(True)], delimiter=';', dtype=str, index_col=None, usecols=["PATIENTID",  "SEX", "BIRTHDATE", "SHEDULEDATE", "EXAMID", "TYPE",
                                                                                                                                                                "MKBCODE"]))

            options.display.max_columns = 7
            options.display.max_rows = 500000
            options.display.width = 200
            return df[df['PATIENTID'] == f'{patient_id}']
        else: raise AssertionError("Пациент не найден!")

    @cache
    async def __check_sheludate(self, i):
        data = i.split(".")
        if not (len(data) == 3 and data[0].isdigit() and data[1].isdigit() and data[
            2].isdigit()): return "Неверный формат даты Sheludate (день, месяц, год)"
        return False


    @cache
    async def __check_birthday(self, i):
        data = i.split(".")
        if not (len(data) == 3 and data[0].isdigit() and data[1].isdigit() and data[2].isdigit()): return "Неверный формат даты Birthday (день, месяц, год)"
        return False
    @cache
    async def __chect_sex(self, i):
        if not (i in ('0', "1") and i.isdigit()): return "Неверный пол! (0 - мужской, 1 - женский)"
        return False
    @cache
    async def __check_type(self, i):
        if not (i in ("1", "2", "3") and i.isdigit()): return "Неверный тип болезни (1 – основной, 2 – конкурирующий, 3 – осложнение)"
        return False
    @cache
    async def __check_id_other(self, i):
        if not (i.isdigit()): return "Неверный формат ID (только число)"
        return False

    @cache
    async def __check_examid(self, i):
        if not (i.isdigit()): return "Неверный формат Examid (только число)"
        return False

    @cache
    async def checker(self, ID = None, Sheludate = None, Sex = None, Birthday = None, Type = None, Mkbcode = None, Examid = None):
        return await gather(*[create_task(self.__check_id_other(ID)), create_task(self.__check_sheludate(Sheludate)), create_task(self.__chect_sex(Sex)), create_task(self.__check_birthday(Birthday)),
                create_task(self.__check_type(Type)), create_task(self.__check_examid(Examid))])



    @cache
    async def delete_line(self, patient_id, number_line):
        time_result = []
        for i in self.__id_database_var.values(): time_result.append(
            create_task(self.__find_patient(tuple(i), patient_id)))
        result = await gather(*time_result)
        if any(result):
            var = self.__file_path + self.__list_files[result.index(True)]
            df = DataFrame(read_csv(var, delimiter=';', dtype=str, index_col=None))
            df = df.drop(number_line)
            df.to_csv(var, sep=";", index=False)
        else:
            raise AssertionError("Пациент не найден!")












