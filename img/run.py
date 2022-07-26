# Загружаем необходимые библиотеки
import os
import simplecrypt
import tempfile
import openpyxl
from openpyxl import Workbook, load_workbook
from openpyxl.writer.excel import save_workbook
import getpass
import stdiomask


# Переход в основную папку программы
def_dir = os.chdir('..')
start_dir = os.chdir('bases')


# Блок начального меню
def start_menu():
	list_start_dir = os.listdir()
	clear_list = [element.replace('.xlsm', '') for element in list_start_dir]
	print("")
	print(" KeePassIc")
	print("")
	print("Базы паролей:",clear_list)
	print("")
	print(" '1' --- Создать базу паролей")
	print("")
	print(" '2' --- Удалить базу паролей")	
	print("")
	print(" '3' --- Открыть базу паролей")
	print("")
	print(" '4' --- Переименовать базу паролей")
	print("")
	print(" '5' --- Изменить ключ шифрования базы паролей")
	print("")
	print(" '6' --- Удалить ключи шифрования")
	print("")	
	print(" '7' --- Выйти из программы")
	print("")
	
	
# Блок работы с начальным меню	
def start_menu_do():
	try:
		doit = input("Выберите действие: ")
	except EOFError:
		os.system('clear')
		exit()
	if doit == '7':
		os.system('clear')
		exit()
	elif doit == '1':
		add_pass_base_menu()
	elif doit == '3':
		open_pass_base_menu()
	elif doit == '2':
		del_pass_base_menu()
	elif doit =='4':
		rename_base_pases()
	elif doit == '5':
		cha_key_base_pase()
	elif doit == '6':
		del_all_keys()
	else:
		print("Такой функции нет! Повторите попытку!")
		start_menu_do()
		
		
# Блок меню создания базы паролей		
def add_pass_base_menu():
	try:
		add_pass_base_menu_do = input("Введите имя базы паролей\n'1' что бы вернуться назад\n'2' чтобы выйти.\nВвод: ")
	except EOFError:
		os.system('clear')
		exit()
	if add_pass_base_menu_do == '2':
		os.system('clear')
		exit()
	elif add_pass_base_menu_do == '1':
		os.system('clear')
		running()
	elif add_pass_base_menu_do == '':
		print ("Имя не может быть пустым")
		add_pass_base_menu()
	elif os.path.isfile(add_pass_base_menu_do + ".nfr"):
		print("База с таким именем уже есть! Пвоторите попытку")
		add_pass_base_menu()
	else:	
		pas_input = stdiomask.getpass("Введите ключ шифрования: ")		

		wb = Workbook()
		ws = wb.active
		ws.title = ' '
		xl_sv = wb.save(add_pass_base_menu_do + '.xlsm')
		
		text_open = open(add_pass_base_menu_do + '.xlsm', 'rb')
		txt = text_open.read()
		text_open.close()
		os.remove(add_pass_base_menu_do + '.xlsm')
		pas = pas_input
		print("\nПодождите идет создание базы паролей")	
		cipher = simplecrypt.encrypt(pas, txt)
		fin = open(add_pass_base_menu_do + '.xlsm', 'wb')
		fin.write(cipher)
		fin.close()
		print("")
		print("База [" + add_pass_base_menu_do + "] создана")
		sv_key = input("1.Сохранить ключ шифрования\nВвод: ")
		if sv_key == '1':
			text_pas = pas_input
			key_pas = 'def@ult_pa$$word' #В кавычках '' можете задать любой набор символо на ваш выбор
			print ("Подождите идет сохранение ключа")
			crypt_pas = simplecrypt.encrypt(key_pas,text_pas)
			os.chdir('..')
			os.chdir('keys')			
			op_sv_key = open("key." + add_pass_base_menu_do + ".nfr", 'wb')
			op_sv_key.write(crypt_pas)
			op_sv_key.close()
			print("Ключ [" + "key." + add_pass_base_menu_do + "] сохранен!")
			os.chdir('..')
			os.chdir('bases')
			
			
		running()
		

# Блок удаления базы паролей
def del_pass_base_menu():
	try:
		del_pass_base_menu_do = input("Введите имя базы паролей\n'1' что бы вернуться назад\n'2' чтобы выйти.\nВвод: ")
	except EOFError:
		os.system('clear')
		exit()
	if del_pass_base_menu_do == '2':
		os.system('clear')
		exit()
	elif del_pass_base_menu_do == '1':
		os.system('clear')
		running()
	elif del_pass_base_menu_do == '':
		print ("Имя не может быть пустым")
		del_pass_base_menu()
	else:
		try:
			os.remove(del_pass_base_menu_do + ".xlsm")
		except FileNotFoundError: 
			print("Такой базы не существует! Повторите попытку.")
			del_pass_base_menu()
		print("")
		print("База [" + del_pass_base_menu_do + "] удалена")
		del_key_pas = input("1.Удалить ключ\n'Enter' продолжить\nВвод: ")
		if del_key_pas == '1':
			os.chdir('..')
			os.chdir('keys')
			try:
				os.remove("key." + del_pass_base_menu_do + ".nfr")
			except FileNotFoundError:
				print("Ключа не существует")
				os.chdir('..')
				os.chdir('bases')
				running()
			print("Ключ [" + "key." + del_pass_base_menu_do + "] удален!")
			os.chdir('..')
			os.chdir('bases')
			running()
		else:
			running()
		

# Блок удаления ключей шифрования
def del_all_keys():
	os.chdir('..')
	os.chdir('keys')
	list_dir = os.listdir()
	clear_list = [element.replace('.nfr', '') for element in list_dir]
	print("Ключи:", clear_list)
	sel_key = input("Введите имя файла ключа\n1.Назад\n2.Выход\nВвод: ")
	if sel_key == '1':
		os.chdir('..')
		os.chdir('bases')
		running()
	elif sel_key == '2':
		os.system('clear')
		exit()
	else:
		try:	
			os.remove(sel_key + ".nfr")
			print("Ключ [" + sel_key + "] удален")
		except FileNotFoundError:
			print("Ключа не существует")
			os.chdir('..')
			os.chdir('bases')
			del_all_keys()
	os.chdir('..')
	os.chdir('bases')
	running()

#Блок переименования базы паролей
def rename_base_pases():
	
	rename_base_pases_do = input("Введите имя базы паролей\n1.Вернуться назад\n2.Выйти\nВвод: ")
	if rename_base_pases_do == '1':
		running()		
	elif rename_base_pases_do == '2':
		os.system('clear')
		exit()
	else:
		new_name_base_pases = input("Введите новое имя базы паролей: ")
		fil = open(rename_base_pases_do + ".xlsm", 'rb')
		inf = fil.read()
		fil.close()
		os.remove(rename_base_pases_do + ".xlsm")
		print("Подождите идет переименование базы паролей")		
		crypt = open(new_name_base_pases + '.xlsm', 'wb')
		crypt.write(inf)
		crypt.close()
		print ("База паролей переименована")
		running()


#Блок изменения ключа шифрования базы паролей
def cha_key_base_pase():
	menu = input("Введите имя базы паролей\n1.Вернуться назад\n2.Выйти\nВвод: ")
	if menu == '1':
		running()		
	elif menu == '2':
		os.system('clear')
		exit()
	else:
		sel_var = input("1.Загрузить файл ключа\n'Enter' для ввода ключа\nВвод: ")
		if sel_var == '1':
			os.chdir('..')
			os.chdir('keys')
			list_dir = os.listdir()
			clear_list = [element.replace('.nfr', '') for element in list_dir]
			print("Ключи:", clear_list)
			sel_text = input("Введите имя файла ключа: ")
			fwk = open(sel_text+".nfr", 'rb')
			text_pas = fwk.read()
			key_pas = 'def@ult_pa$$word' #В кавычках '' можете задать любой набор символо на ваш выбор
			print ("Подождите идет загрузка ключа")
			check_key_base_pase = simplecrypt.decrypt(key_pas,text_pas)
			os.chdir('..')			
			os.chdir('bases')
		else:
			check_key_base_pase = stdiomask.getpass("Введите ключ шифрования базы паролей: ")
			
		fil = open(menu + ".xlsm", 'rb')
		inf = fil.read()
		fil.close()
		pas = check_key_base_pase
		print("Подождите идет проверка ключа базы паролей")	
		cipher_open_base = simplecrypt.decrypt(pas,inf)
		new_key_base_pase = stdiomask.getpass("Введите новый ключ шифрования базы паролей:")	
		new_pas = new_key_base_pase
		new_text = cipher_open_base
		print ("Подождите идет изменение ключа базы паролей")
		cipher_new_base = simplecrypt.encrypt(new_pas,new_text)
		os.remove(menu + ".xlsm")	
		crypt = open(menu + '.xlsm', 'wb')
		crypt.write(cipher_new_base)
		crypt.close()
		print ("Ключ изменен")
		sv_key = input("1.Сохранить ключ шифрования\nВвод: ")
		if sv_key == '1':
			text_pas = new_pas
			key_pas = 'def@ult_pa$$word' #В кавычках '' можете задать любой набор символо на ваш выбор
			print ("Подождите идет сохранение ключа")
			crypt_pas = simplecrypt.encrypt(key_pas,text_pas)
			os.chdir('..')
			os.chdir('keys')			
			op_sv_key = open("key." + menu + ".nfr", 'wb')
			op_sv_key.write(crypt_pas)
			op_sv_key.close()
			print("Ключ [" + "key." + menu + "] сохранен!")
			os.chdir('..')
			os.chdir('bases')
		running()
		
	
			

	
# Блок открытия базы паролей	
def open_pass_base_menu():
	global open_pass_base_menu_do
	try:
		open_pass_base_menu_do = input("Введите имя базы паролей\n'1' что бы вернуться назад\n'2' чтобы выйти.\nВвод: ")
	except EOFError:
		os.system('clear')
		exit()
	if open_pass_base_menu_do == '2':
		os.system('clear')
		exit()
	elif open_pass_base_menu_do == '1':
		os.system('clear')
		running()
	elif open_pass_base_menu_do == '':
		print ("Имя не может быть пустым")
		open_pass_base_menu()
		
	else:
		global key_pass_base
		sel_var = input("1.Загрузить файл ключа\n'Enter' для ввода ключа\nВвод: ")
		if sel_var == '1':
			os.chdir('..')
			os.chdir('keys')
			list_dir = os.listdir()
			clear_list = [element.replace('.nfr', '') for element in list_dir]
			print("Ключи:", clear_list)
			sel_text = input("Введите имя файла ключа\n1.Выйти в меню\nВвод: ")
			if sel_text == '1':
				os.chdir('..')
				os.chdir('bases')
				running()
			try:
				fwk = open(sel_text + '.nfr', 'rb')
			except FileNotFoundError:
				print("Такого ключа нет")
				os.chdir('..')
				os.chdir('bases')
				running()
			text_pas = fwk.read()
			key_pas = 'def@ult_pa$$word' #В кавычках '' можете задать любой набор символо на ваш выбор
			print ("Подождите идет загрузка ключа")
			key_pass_base = simplecrypt.decrypt(key_pas,text_pas)
			os.chdir('..')
			os.chdir('bases')				

		else:
			key_pass_base = stdiomask.getpass("Введите ключ шифрования: ")
		
		work_with_pass_base()
		


# Блок работы с базой паролей
def work_with_pass_base():
	global base_pase
	try:
		fil = open(open_pass_base_menu_do + ".xlsm", 'rb')
	except FileNotFoundError:
			print("Такой базы не существует! Повторите попытку.")
			open_pass_base_menu()	
	inf = fil.read()
	fil.close()
	pas = key_pass_base
	print("Подождите идет открытие базы паролей")	
	cipher_open_base = simplecrypt.decrypt(pas,inf)	
	fold = os.getcwd()			
	temp = tempfile.NamedTemporaryFile(dir = fold,mode = 'w+b')			
	temp.write(cipher_open_base)
	base_pase = openpyxl.load_workbook(temp)
	temp.close()
	print("Аккаунты: ", base_pase.sheetnames) 
	try:
		work_with_pass_base_do = input("1.Посмотреть аккаунт\n2.Добавить аккаунт\n3.Удалить аккаунт\n4.Удалить ключ шифрования\n5.Вернуться назад\n6.Выйти\nВвод: ")
	except EOFError:
    		os.system('clear')
    		exit()

	if work_with_pass_base_do == '6':
		os.system('clear')
		temp.close()
		exit()

	elif work_with_pass_base_do =='5':
		os.system('clear')
		temp.close()
		running()

	elif work_with_pass_base_do =='4':
		del_key_pas()

	elif work_with_pass_base_do =='3':
		del_acc()
		
	elif work_with_pass_base_do =='2':
		create_acc()
	
	elif work_with_pass_base_do =='1':
		work_with_acc()
	
	else:
		print("Такой функции нет! Повторите попытку.")
		work_with_pass_base()	

		
#Блок просмотра аккаунта
def work_with_acc():
	global name_acc_do
	name_acc_do = input("Введите имя аккаунта: ")
	ws = base_pase[name_acc_do]
	ws1 = ws['A1'].value
	ws2 = ws['B1'].value
	ws3 = ws['A2'].value
	ws4 = ws['B2'].value
	ws5 = ws['A3'].value
	ws6 = ws['B3'].value
	print("")
	print("Имя аккаунта:", name_acc_do)
	print(ws1, ws2)
	print(ws3, ws4)
	print(ws5, ws6)
	print("")
	variants = input("1.Изменить аккаунт\n2.Вернуться назад\nВвод: ")
	if variants == '1':
		chan_acc()
	elif variants == '2':
		work_with_pass_base()
	
	
#Блок удаления аккаунта
def del_acc():
	try:
		del_acc_input = input("Введите имя удаляемого аккаунта\n1.Вернуться назад\nВвод: ")
	except EOFError:
    		os.system('clear')
    		exit()
	if del_acc_input == '1':
		work_with_pass_base()
	else:
		targ = base_pase[del_acc_input]
		base_pase.remove(targ)
		sv2 = base_pase.save(open_pass_base_menu_do + '.xlsm')
		text_open = open(open_pass_base_menu_do + '.xlsm', 'rb')
		txt = text_open.read()
		text_open.close()
		os.remove(open_pass_base_menu_do + '.xlsm')
		pas = key_pass_base
		print("\nПодождите идет удаление аккаунта")	
		cipher = simplecrypt.encrypt(pas, txt)
		fin = open(open_pass_base_menu_do + '.xlsm', 'wb')
		fin.write(cipher)
		fin.close()
	
	work_with_pass_base()
	

#Блок удаления ключа шифрования
def del_key_pas():
	os.chdir('..')
	os.chdir('keys')
	try:
		os.remove("key." + open_pass_base_menu_do + ".nfr")
	except FileNotFoundError:
		print("Ключа не существует")
		os.chdir('..')
		os.chdir('bases')
		work_with_pass_base()
	print("Ключ [" + "key." + open_pass_base_menu_do + "] удален!")
	os.chdir('..')
	os.chdir('bases')
	work_with_pass_base()


#Блок создания аккаунта
def create_acc():
	cr_acc_name = input("Введи имя аккаунта: ")
	cr_acc_log = input("Введи логин: ")
	cr_acc_pas = input("Введи пароль: ")
	cr_acc_add = input("Введи доп. информацию: ")
	base_pase.create_sheet(cr_acc_name)			
	ws = base_pase[cr_acc_name]
	ws['A1']='Логин:'
	ws['B1']=cr_acc_log
	ws['A2']='Пароль:'
	ws['B2']=cr_acc_pas
	ws['A3']='Доп.информация:'
	ws['B3']=cr_acc_add
	sv2 = base_pase.save(open_pass_base_menu_do + '.xlsm')
	text_open = open(open_pass_base_menu_do + '.xlsm', 'rb')
	txt = text_open.read()
	text_open.close()
	os.remove(open_pass_base_menu_do + '.xlsm')
	pas = key_pass_base
	print("\nПодождите идет сохранение аккаунта")	
	cipher = simplecrypt.encrypt(pas, txt)
	fin = open(open_pass_base_menu_do + '.xlsm', 'wb')
	fin.write(cipher)
	fin.close()
	work_with_pass_base()
	

#Блок изменения аккаунта
def chan_acc():
	select_vr = input("1.Изменить имя аккаунта\n2.Изменить логин\n3.Изменить пароль\n4.Изменить Доп.Информацию\n5.Вернуться назад\nВвод: ")
	if select_vr =='1':
		chan_acc_name()
	elif select_vr =='2':
		chan_acc_log()
	elif select_vr =='3':
		chan_acc_pas()
	elif select_vr =='4':
		chan_acc_add()
	elif select_vr =='5':
		work_with_pass_base()


#Блок изменения имени аккаунта
def chan_acc_name():

	new_name_acc = input("Введите новое имя аккаунта: ")
	ws = base_pase[name_acc_do]
	ws.title = new_name_acc
	sv2 = base_pase.save(open_pass_base_menu_do + '.xlsm')
	text_open = open(open_pass_base_menu_do + '.xlsm', 'rb')
	txt = text_open.read()
	text_open.close()
	os.remove(open_pass_base_menu_do + '.xlsm')
	pas = key_pass_base
	print("\nПодождите идет сохранение изменений")	
	cipher = simplecrypt.encrypt(pas, txt)
	fin = open(open_pass_base_menu_do + '.xlsm', 'wb')
	fin.write(cipher)
	fin.close()

	work_with_pass_base()
	

#Блок изменения логина аккаунта
def chan_acc_log():
	new_name_login = input("Введите новый логин: ")
	ws = base_pase[name_acc_do]
	ws['B1']=new_name_login
	sv2 = base_pase.save(open_pass_base_menu_do + '.xlsm')
	text_open = open(open_pass_base_menu_do + '.xlsm', 'rb')
	txt = text_open.read()
	text_open.close()
	os.remove(open_pass_base_menu_do + '.xlsm')
	pas = key_pass_base
	print("\nПодождите идет сохранение изменений")	
	cipher = simplecrypt.encrypt(pas, txt)
	fin = open(open_pass_base_menu_do + '.xlsm', 'wb')
	fin.write(cipher)
	fin.close()

	work_with_pass_base()


#Блок изменения пароля аккаунта
def chan_acc_pas():
	new_name_pas = input("Введите новый пароль: ")
	ws = base_pase[name_acc_do]
	ws['B2']=new_name_pas
	sv2 = base_pase.save(open_pass_base_menu_do + '.xlsm')
	text_open = open(open_pass_base_menu_do + '.xlsm', 'rb')
	txt = text_open.read()
	text_open.close()
	os.remove(open_pass_base_menu_do + '.xlsm')
	pas = key_pass_base
	print("\nПодождите идет сохранение изменений")	
	cipher = simplecrypt.encrypt(pas, txt)
	fin = open(open_pass_base_menu_do + '.xlsm', 'wb')
	fin.write(cipher)
	fin.close()

	work_with_pass_base()


#Блок изменения Доп.информации аккаунта		
def chan_acc_add():
	new_name_add = input("Введите новую Доп.информацию: ")
	ws = base_pase[name_acc_do]
	ws['B3']=new_name_add
	sv2 = base_pase.save(open_pass_base_menu_do + '.xlsm')
	text_open = open(open_pass_base_menu_do + '.xlsm', 'rb')
	txt = text_open.read()
	text_open.close()
	os.remove(open_pass_base_menu_do + '.xlsm')
	pas = key_pass_base
	print("\nПодождите идет сохранение изменений")	
	cipher = simplecrypt.encrypt(pas, txt)
	fin = open(open_pass_base_menu_do + '.xlsm', 'wb')
	fin.write(cipher)
	fin.close()

	work_with_pass_base()


# Блок запуска программы(В самый конец кода)
def running():
	start_menu()
	start_menu_do()
	

# Запуск программы	
running()
