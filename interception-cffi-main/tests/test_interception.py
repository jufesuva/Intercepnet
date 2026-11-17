from __future__ import annotations

from typing import Any

from interception import ffi, lib


def send_key_event(context, device, key_code: int, state: int):
    """Envía un evento de teclado."""
    stroke = ffi.new('InterceptionKeyStroke *', {'code': key_code, 'state': state, 'information': 0})
    lib.interception_send(context, device, stroke, 1)
    print(f"Key event sent - code: {key_code}, state: {state}")


def send_mouse_event(context, device, state: int, flags: int):
    """Envía un evento de ratón."""
    stroke = ffi.new('InterceptionMouseStroke *', {'state': state, 'flags': flags, 'rolling': 0, 'x': 0, 'y': 0, 'information': 0})
    lib.interception_send(context, device, stroke, 1)
    print(f"Mouse event sent - state: {state}, flags: {flags}")


def simulate_and_capture_key(context, device, key_code: int):
    """Simula la presión de una tecla y captura el evento."""
    # Simular la presión de la tecla
    send_key_event(context, device, key_code, lib.INTERCEPTION_KEY_DOWN)  # Presionar 'E'
    send_key_event(context, device, key_code, lib.INTERCEPTION_KEY_UP)    # Soltar 'E'

    # Capturar el evento generado
    print("Capturing the simulated key event...")
    stroke = ffi.new('InterceptionKeyStroke *')
    if lib.interception_receive(context, device, stroke, 1) > 0:
        print(f"Simulated key event captured - code: {stroke.code}, state: {stroke.state}")
        return stroke.code
    else:
        print("Failed to capture the simulated key event.")
        return None

def test_real_events():
    context = lib.interception_create_context()
    if context == 0:
        print("Error: Context could not be created.")
        return

    print("Context successfully created.")

    # Detectar dispositivos
    print("Detecting devices...")
    for device in range(1, 11):  # Interception soporta hasta 10 dispositivos
        print(f"Checking device {device}...")
        stroke = ffi.new('InterceptionKeyStroke *')
        if lib.interception_receive(context, device, stroke, 1) > 0:
            print(f"Device {device} is active and receiving events.")
        else:
            print(f"Device {device} is not active.")

    # Capturar eventos sin filtrar
    print("Testing raw event capture...")
    while True:
        device = lib.interception_wait(context)
        print(f"Device detected: {device}")
        stroke = ffi.new('InterceptionKeyStroke *')
        if lib.interception_receive(context, device, stroke, 1) > 0:
            print(f"Raw event captured - device: {device}, code: {stroke.code}, state: {stroke.state}")
            break

    lib.interception_destroy_context(context)
    print("Context destroyed.")

if __name__ == "__main__":
    print("Running test_real_events...")
    test_real_events()