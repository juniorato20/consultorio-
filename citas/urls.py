from rest_framework import routers
from .viewset import *

router = routers.SimpleRouter()
router.register('api/reporte',ReporteViewset)
router.register('api/cita',CitaViewset)
router.register('api/doctor',DoctorViewset)
router.register('api/paciente',PacienteViewset)

urlpatterns = router.urls