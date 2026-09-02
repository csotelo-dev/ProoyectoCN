"""Middleware de auditoría — registra operaciones de escritura."""

import logging

from .models import RegistroAuditoria

logger = logging.getLogger("core.audit")


class AuditMiddleware:
    """Registra cada petición POST/PUT/PATCH/DELETE de usuarios autenticados."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            request.user.is_authenticated
            and request.method in ("POST", "PUT", "PATCH", "DELETE")
            and response.status_code < 400
        ):
            accion_map = {
                "POST": "CREATE",
                "PUT": "UPDATE",
                "PATCH": "UPDATE",
                "DELETE": "DELETE",
            }
            try:
                RegistroAuditoria.objects.create(
                    usuario=request.user,
                    accion=accion_map.get(request.method, "UPDATE"),
                    modelo=request.path,
                    detalle=f"{request.method} {request.path}",
                    ip_address=self._get_client_ip(request),
                )
            except Exception:
                logger.exception("Error al registrar auditoría")

        return response

    @staticmethod
    def _get_client_ip(request):
        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded:
            return x_forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
