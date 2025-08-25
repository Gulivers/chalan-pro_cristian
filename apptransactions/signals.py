"""
Sistema de Señales para Gestión Automática de Inventario

Este módulo implementa señales de Django que automatizan la sincronización
entre transacciones de documentos y movimientos de inventario.

Funcionalidades: oahp
- Crear/actualizar movimientos de inventario al guardar líneas de documento
- Eliminar movimientos de inventario al eliminar líneas de documento
- Manejo automático de entradas/salidas de productos en almacenes
- Consistencia de datos mediante transacciones atómicas

Autor: Sistema Chalan-Pro
"""

from decimal import Decimal
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from apptransactions.models import DocumentLine
from appinventory.models import InventoryMovement


@receiver(post_save, sender=DocumentLine, dispatch_uid="docline_create_inventory_movement")
def create_inventory_movement(sender, instance, **kwargs):
    print("  2 🧼 apptransactions\\signals.py -> create_inventory_movement()")
    
    def handle_movement():
        try:
            warehouse = instance.warehouse or instance.document.warehouse
            doc_type = instance.document.document_type
            movement_type = doc_type.stock_movement

            if not warehouse or movement_type == 0:
                print("🚫 No se crea movimiento: documento neutro o sin almacén.")
                return

            print(f"🔄 Preparando movimiento para línea {instance.id} | Producto: {instance.product} | Cantidad: {instance.quantity}")

            # Revisa si ya existe un movimiento para esa línea
            movement = InventoryMovement.objects.filter(line_id=instance.id).first()

            if movement:
                print(f"♻️ Actualizando movimiento existente para línea {instance.id}")
                movement.product = instance.product
                movement.warehouse = warehouse
                movement.quantity = instance.quantity
                movement.movement_type = movement_type
                movement.unit = instance.unit
                movement.reason = f"{doc_type.description} #{instance.document.id}"
                movement.document = str(instance.document.id)
                movement.created_by = instance.document.created_by
            else:
                print(f"🆕 Creando nuevo movimiento para línea {instance.id}")
                movement = InventoryMovement(
                    line_id=instance.id,
                    product=instance.product,
                    warehouse=warehouse,
                    quantity=instance.quantity,
                    movement_type=movement_type,
                    unit=instance.unit,
                    reason=f"{doc_type.description} #{instance.document.id}",
                    document=str(instance.document.id),
                    created_by=instance.document.created_by
                )

            movement.save()
            print(f"✅ Movimiento de inventario guardado para línea {instance.id}")

        except Exception as e:
            print(f"❌ Error en handle_movement(): {e}")

    transaction.on_commit(handle_movement)


@receiver(post_delete, sender=DocumentLine, dispatch_uid="docline_delete_inventory_movement")
def delete_inventory_movement(sender, instance, **kwargs):
    def handle_deletion():
        try:
            InventoryMovement.objects.filter(line_id=instance.id).delete()
            print(f"🗑️ Movimiento eliminado para línea {instance.id}")
        except Exception as e:
            print(f"❌ Error al eliminar movimiento para línea {instance.id}: {e}")

    transaction.on_commit(handle_deletion)
