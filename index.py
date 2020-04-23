from tkinter import ttk
from tkinter import *
import sqlite3 as sql

class Product:

	db_name = 'db_constructora.db'

	def __init__(self, window):
		self.wind = window
		self.wind.title('Administrador de BD *Constructora*')
		self.wind.resizable(0,0)

		#Creando el Frame
		frame = LabelFrame(self.wind, text= 'Registra un nuevo producto')
		frame.grid(row=0, column=0, columnspan=3, pady=20, padx=10)
		
		#Entrade de nombre
		Label(frame, text='Nombre: ').grid(row=1, column=0, padx=5, pady=2)
		self.nombre = Entry(frame)
		self.nombre.focus()
		self.nombre.grid(row=1,column=1, padx=5, pady=2)

		#Entrada precio
		Label(frame, text='Precio: ').grid(row=2, column=0, padx=5, pady=2)
		self.precio = Entry(frame)
		self.precio.grid(row=2,column=1, padx=5, pady=2)

		#Botón agregar producto
		Button(frame, text='Guardar producto', command=self.addProduct).grid(row=3, columnspan=2, sticky=W+E, pady=2, padx=5)

		#Mensajes en pantalla
		self.mensaje = Label(text='', fg='red')
		self.mensaje.grid(row=5, column=0, columnspan=2, sticky=W+E)
		Label(text='').grid(row=6)

		#Tabla de la BD
		self.tree = ttk.Treeview(height=10, columns=2)
		self.tree.grid(row=7, padx=5, pady=2, columnspan=2)
		self.tree.heading('#0', text='Nombre', anchor=CENTER)
		self.tree.heading('#1', text='Precio', anchor= CENTER)

		#Botón borrar producto
		Button(text='Borrar', command=self.deleteProduct).grid(row=8, column=0, padx=5, pady=2, sticky=W+E)

		#Botón editar producto
		Button(text='Editar', command = self.editProduct).grid(row=8, column=1, padx=5, pady=2, sticky=W+E)

		#Listar datos
		self.getProducts()

	def run_query(self, query, parametros=()):
		with sql.connect(self.db_name) as conn:
			cursor = conn.cursor()
			result = cursor.execute(query, parametros)
			conn.commit()
		return result

	def getProducts(self):
		#Limpiando la tabla
		records = self.tree.get_children()
		for element in records:
			self.tree.delete(element)
		#Realizando consulta en la BD
		query = 'SELECT * FROM product ORDER BY nombre DESC'
		db_rows = self.run_query(query)
		#Insertando los datos de la BD en la tabla
		for row in db_rows:
			self.tree.insert('', 0, text=row[1], values=row[2])

	def validar(self):
		return len(self.nombre.get())!=0 and len(self.precio.get())!=0

	def addProduct(self):
		if self.validar():
			query = 'INSERT INTO product VALUES(NULL, ?, ?)'
			parametros = (self.nombre.get(), self.precio.get())
			self.run_query(query, parametros)
			self.mensaje['text'] = 'Producto {} agregado'.format(self.nombre.get())
			self.nombre.delete(0, END)
			self.precio.delete(0, END)
		else:
			self.mensaje['text'] = 'Ambos campos son requeridos'
		self.getProducts()

	def deleteProduct(self):
		self.mensaje['text'] = ''
		try:
			self.tree.item(self.tree.selection())['text'][0]
		except IndexError as e:
			self.mensaje['text'] = 'Selecciona un registro'
			return
		self.mensaje['text'] = ''
		name = self.tree.item(self.tree.selection())['text']
		query = 'DELETE FROM product WHERE nombre = ?'
		self.run_query(query, (name,))
		self.mensaje['text'] = 'Se ha eliminado el producto: {}'.format(name)
		self.getProducts()

	def editProduct(self):
		self.mensaje['text'] = ''
		try:
			self.tree.item(self.tree.selection())['text'][0]
		except IndexError as e:
			self.mensaje['text'] = 'Selecciona un registro'
			return

		old_name = self.tree.item(self.tree.selection())['text']
		old_price = self.tree.item(self.tree.selection())['values'][0]
		self.editWind = Toplevel()
		self.editWind.title = 'Editar producto'
		self.editWind.resizable(0,0)
		self.editWind.focus()

		#Old Name
		Label(self.editWind, text='Nombre anterior: ').grid(row=0, column=0, padx=5, pady=2)
		Entry(self.editWind, textvariable=StringVar(self.editWind, value=old_name), state='readonly').grid(row=0, column=1, padx=5, pady=2)
		#New Name
		Label(self.editWind, text='Nuevo nombre: ').grid(row=1, column=0, padx=5, pady=2)
		new_Name = Entry(self.editWind)
		new_Name.grid(row=1, column=1, padx=5, pady=2)
		new_Name.focus()

		#Old Price
		Label(self.editWind, text='Precio anterior: ').grid(row=2, column=0, padx=5, pady=2)
		Entry(self.editWind, textvariable=StringVar(self.editWind, value=old_price), state='readonly').grid(row=2, column=1, padx=5, pady=2)
		#New Price
		Label(self.editWind, text='Nuevo precio: ').grid(row=3, column=0, padx=5, pady=2)
		new_Price = Entry(self.editWind)
		new_Price.grid(row=3, column=1, padx=5, pady=2)

		#Boton actualizar
		Button(self.editWind, text='Actualizar', command = lambda: self.editRecord(new_Name.get(), old_name, new_Price.get(), old_price)).grid(row=4, columnspan=2, padx=5, pady=2, sticky=W+E)

	def editRecord(self, new_name, old_name, new_price, old_price):
		query = 'UPDATE product SET nombre = ?, precio = ? WHERE nombre = ? AND precio = ?'
		parametros = (new_name, new_price, old_name, old_price)
		self.run_query(query, parametros)
		self.editWind.destroy()
		self.mensaje['text'] = 'El registro {} ha sido actualizado a {}'.format(old_name ,new_name)
		self.getProducts()

#Condición para saber si se ejecuta
if __name__ == '__main__':
	window = Tk()
	application = Product(window)
	window.mainloop()