from opentelemetry import trace

def init_tracer(service: str) -> None:
    trace.set_tracer_provider(trace.TracerProvider())
    trace.get_tracer(service)
