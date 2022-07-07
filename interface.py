from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import telegram
import crypto


mode = -1
image_expansion = ['png', 'jpg']


def login():
    def accept_login(password):
        global mode
        mode = crypto.vereficate_password(password)
        if mode == 0 or mode == 1:
            login_page.destroy()
        else:
            messagebox.showerror(title='ERROR', message='WRONG PASSWORD')

    login_page = Tk()

    password = StringVar()

    login_page.title('LOGIN')
    login_page.geometry('200x100')

    Label(login_page, text='PASSWORD:').grid(row=0, column=0, padx=(40, 0))
    Entry(login_page, show='*', textvariable=password).grid(row=1, column=0, padx=(40, 0))
    Button(login_page, text='Enter', command=lambda: accept_login(password.get())).grid(row=3, column=0, pady=(10, 0),
                                                                                        padx=(40, 0))
    login_page.mainloop()


def main():
    global mode

    def set_listbox():
        listbox.delete(0, END)
        for file in telegram.search_message(mode):
            listbox.insert(END, file['file_name'])

    def delete_message():
        need_file = listbox.get(listbox.curselection())
        for file in telegram.search_message(mode):
            if need_file == file['file_name']:
                telegram.delete_message(file['message_id'])
                break

    def download_file():
        def image_param(file_name):
            def work(decrypt, message):
                if decrypt:
                    crypto.decrypt('./TEMP/', file_name)
                if message:
                    messagebox.showinfo(title='MESSAGE', message=crypto.stega_decrypt(f'./TEMP/{file_name}', filedialog.askopenfilename(title='patch to keys')))

                crypto.replace(f'./TEMP/{file_name}', filedialog.askdirectory()+file_name)
                question.destroy()




            question = Tk()

            Decrypt = BooleanVar(question)
            Message = BooleanVar(question)

            Checkbutton(question, text='Message in pic', variable=Message, onvalue=True, offvalue=False).grid(row=0, column=1)
            Checkbutton(question, text='Decrypt', variable=Decrypt, onvalue=True, offvalue=False).grid(row=0, column=0)
            Button(question, text='DOWNLOAD', width=15, command=lambda: work(Decrypt.get(), Message.get())).grid(row=3, column=0, columnspan=2)

            question.mainloop


        need_file = listbox.get(listbox.curselection())
        for file in telegram.search_message(mode):
            if need_file == file['file_name']:
                if need_file.split('.')[-1] == 'png':
                    telegram.download_file(file['file_id'], './TEMP/', need_file, deccrypt=False)
                    image_param(need_file)
                else:
                    telegram.download_file(file['file_id'], filedialog.askdirectory(), need_file)
                    crypto.remove(f'./TEMP/{need_file}')
                break


    def send_file():
        def image_param(patch_to_file, mode):
            def work(encrypt, message):
                if message == '' and encrypt:
                    crypto.crypt(path_to_file, mode)
                elif message == '' and encrypt == False:
                    telegram.send_file(patch_to_file, mode)
                elif message != '' and encrypt:
                    crypto.stega_encrypt(patch_to_file, message,
                                         filedialog.askdirectory())
                    crypto.crypt(f'./TEMP/{patch_to_file.split("/")[-1].replace("jpg", "png")}', mode)
                elif message != '' and encrypt == False:
                    crypto.stega_encrypt(patch_to_file, message,
                                         filedialog.askdirectory())
                    telegram.send_file(f'./TEMP/{patch_to_file.split("/")[-1].replace("jpg", "png")}', mode)

                #crypto.remove(f'./TEMP/{patch_to_file.split("/")[-1].replace("jpg", "png")}')
                question.destroy()
                set_listbox()

            question = Tk()

            question.title(patch_to_file.split('/')[-1])

            Encrypt = BooleanVar(question)
            Message = StringVar(question)

            Checkbutton(question, text='Encrypt', variable=Encrypt, onvalue=True, offvalue=False).grid(row=0, column=0)

            Label(question, text='Message:').grid(row=1, column=0)
            Entry(question, textvariable=Message).grid(row=2, column=0, columnspan=2)

            Button(question, text='SEND', width=15, command=lambda: work(Encrypt.get(), Message.get())).grid(row=3, column=0, columnspan=2)

            question.mainloop()

        path_to_file = filedialog.askopenfilename()
        if path_to_file.split('.')[-1] in image_expansion:
            image_param(path_to_file, mode)
        else:
            crypto.crypt(path_to_file, mode)

    root = Tk()

    root.title('Vault')

    listbox = Listbox(root, selectmode=SINGLE, width=35)
    listbox.grid(row=0, column=0, columnspan=2)

    Button(root, text='REFRESH', width=30, command=lambda: set_listbox()).grid(row=1, column=0)
    Button(root, text='UPLOAD', width=30, command=lambda: send_file()).grid(row=2, column=0)
    Button(root, text='DOWNLOAD', width=30, command=lambda: download_file()).grid(row=3, column=0)
    Button(root, text='DELETE', width=30, command=lambda: [delete_message(), set_listbox()]).grid(row=4, column=0)
    Button(root, text='EXIT', width=30, command=lambda: root.destroy()).grid(row=5, column=0)

    set_listbox()
    root.mainloop()
