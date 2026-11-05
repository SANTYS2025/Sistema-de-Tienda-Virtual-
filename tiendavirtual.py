class Producto:
    def __init__(self, nombre: str, precio: float, stock: int):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def descripcion(self) -> str:
        return f"{self.nombre} - Precio: ${self.precio:.2f} (Stock: {self.stock})"

    def calcular_descuento(self, descuento_base: float = 0, cupon: float = 0, cliente_premium: bool = False) -> float:
        porcentaje_total = descuento_base + cupon
        if cliente_premium:
            porcentaje_total += 5
        return self.precio * (porcentaje_total / 100)

    def calcular_precio_final(self, descuento_base: float = 0, cupon: float = 0, cliente_premium: bool = False) -> float:
        return self.precio - self.calcular_descuento(descuento_base, cupon, cliente_premium)


class ProductoRopa(Producto):
    def descripcion(self) -> str:
        return f"[Ropa] {super().descripcion()}"

    def calcular_descuento(self, descuento_base: float = 0, cupon: float = 0, cliente_premium: bool = False) -> float:
        porcentaje_total = descuento_base + cupon
        if cliente_premium:
            porcentaje_total += 15 
        return self.precio * (porcentaje_total / 100)


class ProductoAlimento(Producto):
    def descripcion(self) -> str:
        return f"[Alimento] {super().descripcion()}"

    def calcular_descuento(self, descuento_base: float = 0, cupon: float = 0, cliente_premium: bool = False) -> float:
        porcentaje_total = descuento_base + cupon + (5 if cliente_premium else 0)
        if porcentaje_total > 20:
            porcentaje_total = 20
        return self.precio * (porcentaje_total / 100)


class ProductoElectronico(Producto):
    def descripcion(self) -> str:
        return f"[Electrónico] {super().descripcion()}"

    def calcular_descuento(self, descuento_base: float = 0, cupon: float = 0, cliente_premium: bool = False) -> float:
        depreciacion = self.precio * 0.10
        precio_depreciado = self.precio - depreciacion
        porcentaje_descuento = descuento_base + cupon + (5 if cliente_premium else 0)
        descuento_adicional = precio_depreciado * (porcentaje_descuento / 100)
        return depreciacion + descuento_adicional


class CarritoDeCompras:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto: Producto):
        self.productos.append(producto)

    def obtener_total(self, descuento_base: float = 0, cupon: float = 0, cliente_premium: bool = False) -> float:
        return sum(p.calcular_precio_final(descuento_base, cupon, cliente_premium) for p in self.productos)


# --- INTERFAZ INTERACTIVA DE CONSOLA ---
def menu_interactivo():
    carrito = CarritoDeCompras()
    
    while True:
        print("\n" + "="*35)
        print("🛒 SISTEMA DE TIENDA VIRTUAL")
        print("="*35)
        print("1. Agregar Ropa al carrito")
        print("2. Agregar Alimento al carrito")
        print("3. Agregar Electrónico al carrito")
        print("4. Ver Carrito y Procesar Pago")
        print("5. Salir")
        
        opcion = input("\nElige una opción (1-5): ")

        if opcion in ['1', '2', '3']:
            try:
                nombre = input("Ingresa el nombre del producto: ")
                precio = float(input("Ingresa el precio del producto: $"))
                stock = int(input("Ingresa el stock disponible: "))
                
                if opcion == '1':
                    nuevo_producto = ProductoRopa(nombre, precio, stock)
                elif opcion == '2':
                    nuevo_producto = ProductoAlimento(nombre, precio, stock)
                elif opcion == '3':
                    nuevo_producto = ProductoElectronico(nombre, precio, stock)
                    
                carrito.agregar_producto(nuevo_producto)
                print(f"✅ ¡'{nombre}' agregado al carrito con éxito!")
            except ValueError:
                print("❌ Error: Por favor ingresa números válidos para el precio y el stock.")

        elif opcion == '4':
            if not carrito.productos:
                print("⚠️ El carrito está vacío. Agrega productos primero.")
                continue
                
            print("\n--- CONFIGURACIÓN DE DESCUENTOS ---")
            try:
                desc_base_str = input("Descuento base (%) [Presiona Enter para 0]: ")
                desc_base = float(desc_base_str) if desc_base_str else 0.0
                
                cupon_str = input("Cupón extra (%) [Presiona Enter para 0]: ")
                cupon = float(cupon_str) if cupon_str else 0.0
                
                premium_str = input("¿El cliente es Premium? (s/n): ").strip().lower()
                es_premium = True if premium_str == 's' else False
                
                print("\n" + "-"*35)
                print("🧾 FACTURA DETALLADA")
                print("-"*35)
                
                # Demostración del polimorfismo
                for prod in carrito.productos:
                    print(prod.descripcion())
                    precio_final = prod.calcular_precio_final(desc_base, cupon, es_premium)
                    print(f"  ↳ Precio con descuento aplicado: ${precio_final:.2f}\n")
                    
                total = carrito.obtener_total(desc_base, cupon, es_premium)
                print("="*35)
                print(f"💰 TOTAL A PAGAR: ${total:.2f}")
                print("="*35)
                
            except ValueError:
                print("❌ Error: Los descuentos deben ser números.")

        elif opcion == '5':
            print("👋 ¡Gracias por usar la Tienda Virtual! Hasta luego.")
            break
            
        else:
            print("❌ Opción no válida. Por favor elige un número del 1 al 5.")

if __name__ == "__main__":
    menu_interactivo()