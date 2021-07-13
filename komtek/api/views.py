from tkinter import *
from tkinter import messagebox

from django.shortcuts import render
from tkcalendar import DateEntry
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.models import Handbook, HandbookSerializer, Item, ItemSerializer


def gui1():
    window = Tk()
    window.title("Добавить справочник")
    lbl1 = Label(window, text="Наименование")
    lbl2 = Label(window, text="Короткое наименование")
    lbl3 = Label(window, text="Описание")
    lbl4 = Label(window, text="Дата начала действия")
    txt = Entry(window, width=40)
    txt2 = Entry(window, width=40)
    txt3 = Entry(window, width=40)
    txt4 = DateEntry(window, width=40)

    def clicked():
        top_handbook = Handbook.objects.order_by('-uid').first()
        el = Handbook(uid=top_handbook.uid + 1, name=txt.get(), short_name=txt2.get(), version=1,
                      description=txt3.get(),
                      date=txt4.get_date())
        el.save()
        messagebox.showinfo('Готово', 'Готово')

    btn = Button(window, text="Отправить", command=clicked)
    lbl1.grid(column=0, row=0)
    lbl2.grid(column=0, row=2)
    lbl3.grid(column=0, row=4)
    lbl4.grid(column=0, row=6)
    btn.grid(column=0, row=10)
    txt.grid(column=0, row=1)
    txt2.grid(column=0, row=3)
    txt3.grid(column=0, row=5)
    txt4.grid(column=0, row=7)
    window.geometry('400x250')
    window.mainloop()


def gui2():
    window = Tk()
    window.title("Новая версия справочника")
    lbl1 = Label(window, text="Введите идентификатор")
    txt = Entry(window, width=40)
    txt4 = DateEntry(window, width=40)
    lbl4 = Label(window, text="Дата начала действия")

    def clicked():
        handbook = Handbook.objects.filter(uid=txt.get()).order_by('-version').first()
        el = Handbook(uid=handbook.uid, name=handbook.name, short_name=handbook.short_name,
                      version=handbook.version + 1,
                      description=handbook.description,
                      date=txt4.get_date())
        el.save()
        messagebox.showinfo('Готово', 'Готово')

    btn = Button(window, text="Отправить", command=clicked)
    lbl1.grid(column=0, row=0)
    lbl4.grid(column=0, row=2)
    btn.grid(column=0, row=10)
    txt.grid(column=0, row=1)
    txt4.grid(column=0, row=3)
    window.geometry('400x250')
    window.mainloop()


def gui3():
    window = Tk()
    window.title("Новая версия справочника")
    lbl1 = Label(window, text="Введите идентификатор")
    txt = Entry(window, width=40)
    txt2 = Entry(window, width=40)
    txt3 = Entry(window, width=40)
    lbl2 = Label(window, text="Код элемента")
    lbl3 = Label(window, text="Значение элемента")

    def clicked():
        handbook = Handbook.objects.filter(uid=txt.get()).order_by('-version').first()
        el = Item(handbook=handbook, code=txt2.get(), value=txt3.get())
        el.save()
        messagebox.showinfo('Готово', 'Готово')

    btn = Button(window, text="Отправить", command=clicked)
    lbl1.grid(column=0, row=0)
    lbl2.grid(column=0, row=2)
    lbl3.grid(column=0, row=4)
    btn.grid(column=0, row=10)
    txt.grid(column=0, row=1)
    txt2.grid(column=0, row=3)
    txt3.grid(column=0, row=5)
    window.geometry('400x250')
    window.mainloop()


def gui(request):
    window = Tk()
    window.title("Меню")
    lbl1 = Label(window, text="Создать новый словарь")
    lbl2 = Label(window, text="Создать новую версию словаря")
    lbl3 = Label(window, text="Добавить элементы в словарь")
    btn = Button(window, text="Отправить", command=gui1)
    btn2 = Button(window, text="Отправить", command=gui2)
    btn3 = Button(window, text="Отправить", command=gui3)
    lbl1.grid(column=0, row=0)
    lbl2.grid(column=0, row=2)
    lbl3.grid(column=0, row=4)
    btn.grid(column=0, row=1)
    btn2.grid(column=0, row=3)
    btn3.grid(column=0, row=5)
    window.geometry('400x250')
    window.mainloop()
    return render(request, 'index.html')


class EzPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class HandbookViewSet(viewsets.ModelViewSet):
    queryset = Handbook.objects.all()
    serializer_class = HandbookSerializer
    pagination_class = EzPagination

    def list(self, request, *args, **kwargs):
        if request.data.get('date') is None:
            queryset = Handbook.objects.all().order_by('-id')
        else:
            queryset = Handbook.objects.filter(date__lte=request.data['date']).order_by('-id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = EzPagination

    def list(self, request, *args, **kwargs):
        if request.data.get('uid') is None:
            queryset = Item.objects.all().order_by('-id')
        else:
            if request.data.get('version') is None:
                top_handbook = Handbook.objects.prefetch_related('items').filter(uid=request.data['uid']).order_by(
                    '-version').first()
                queryset = top_handbook.items.all()
            else:
                queryset = Item.objects.filter(handbook__uid=request.data['uid'],
                                               handbook__version=request.data['version']).order_by('-id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
