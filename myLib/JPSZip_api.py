import zipfile
import os

class ZipHandler:
    def __init__(self, zip_filepath):
        self.zip_filepath = zip_filepath
    
    def create_zip(self):
        if os.path.exists(self.zip_filepath):
            return
        with zipfile.ZipFile(self.zip_filepath, 'w') as zipf:
            pass  # 可以根據需要初始化某些檔案

    def add_file(self, file_name, file_content):
        # 檢查檔案是否已經存在
        with zipfile.ZipFile(self.zip_filepath, 'a') as zipf:
            if file_name in zipf.namelist():
                print(f"Error: '{file_name}' already exists in the ZIP file.")
                return  # 如果檔案已經存在，則不新增
            zipf.writestr(file_name, file_content)

    def modify_file(self, old_file_name, new_file_name, new_file_content):
        temp_zip = self.zip_filepath + ".temp"
        with zipfile.ZipFile(self.zip_filepath, 'r') as zipf, zipfile.ZipFile(temp_zip, 'w') as temp_zipf:
            for file in zipf.namelist():
                if file != old_file_name:
                    temp_zipf.writestr(file, zipf.read(file))
            temp_zipf.writestr(new_file_name, new_file_content)
        os.replace(temp_zip, self.zip_filepath)

    def delete_file(self, file_name):
        temp_zip = self.zip_filepath + ".temp"
        with zipfile.ZipFile(self.zip_filepath, 'r') as zipf, zipfile.ZipFile(temp_zip, 'w') as temp_zipf:
            for file in zipf.namelist():
                if file != file_name:
                    temp_zipf.writestr(file, zipf.read(file))
        os.replace(temp_zip, self.zip_filepath)

    def namelist(self):
        with zipfile.ZipFile(self.zip_filepath, 'r') as zipf:
            return zipf.namelist()
                

    def get_file_data(self, file_name):
        with zipfile.ZipFile(self.zip_filepath, 'r') as zipf:
            if file_name in zipf.namelist():
                file_data = zipf.read(file_name)  # 獲取檔案資料
                return file_data
            else:
                print(f"Error: '{file_name}' not found in the ZIP file.")
                return None  # 若檔案不存在則返回 None