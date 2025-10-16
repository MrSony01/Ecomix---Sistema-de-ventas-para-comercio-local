from django.db import models

class Report(models.Model):
    """
    Generated reports for business intelligence
    """
    REPORT_TYPES = [
        ('sales', 'Ventas'),
        ('inventory', 'Inventario'),
        ('customers', 'Clientes'),
        ('financial', 'Financiero'),
    ]
    
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    date_from = models.DateField()
    date_to = models.DateField()
    generated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='reports/', blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.name} - {self.get_report_type_display()}"
