# otel_app.py

import os
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware

# 1. Configure tracer
resource = Resource.create({SERVICE_NAME: "frappe-app"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# 2. Span processors
otlp_exporter = OTLPSpanExporter(
    endpoint=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "otel-collector:4317"),
    insecure=True
)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

# 3. Import the real WSGI app
from frappe.app import application as frappe_application

# 4. Wrap it in OTEL middleware
application = OpenTelemetryMiddleware(frappe_application)
