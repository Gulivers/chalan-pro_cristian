from django.core.management.base import BaseCommand
from appinventory.models import ProductUnit, UnitConversion
from decimal import Decimal

class Command(BaseCommand):
    help = 'Valida si los precios por unidad están proporcionales según las conversiones'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("🔍 Iniciando validación de unidades y precios..."))

        inconsistencias = 0

        for pu in ProductUnit.objects.select_related('product', 'unit'):
            base_unit = pu.product.unit_default
            if pu.unit == base_unit:
                continue  # Nada que comparar con unidad base

            try:
                conv = UnitConversion.objects.get(from_unit=pu.unit, to_unit=base_unit)
                esperado = Decimal(1) / conv.conversion_factor if conv.sign == '/' else Decimal(conv.conversion_factor)
                if abs(pu.conversion_factor - esperado) > Decimal('0.01'):
                    inconsistencias += 1
                    self.stdout.write(self.style.WARNING(
                        f"⚠️ {pu.product.name} - {pu.unit.code}: "
                        f"esperado {esperado}, tiene {pu.conversion_factor}"
                    ))
            except UnitConversion.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"❌ No se encontró conversión entre {pu.unit.code} → {base_unit.code} "
                    f"para {pu.product.name}"
                ))

        if inconsistencias == 0:
            self.stdout.write(self.style.SUCCESS("✅ Todo en orden. No se encontraron inconsistencias."))
        else:
            self.stdout.write(self.style.ERROR(f"🚨 Se encontraron {inconsistencias} posibles errores."))

