"""
Modulo de teste para o Peanut OS Compact.

Este modulo mostra como os Custom Mods funcionam na v0.3.0.
Todo modulo deve expor uma funcao activate(system), recebendo a instancia do
PeanutCompact. A funcao pode adicionar notificacoes, historico e alterar somente
a memoria simulada do Peanut OS.
"""

MODULE_NAME = "Peanut Test Module"
MODULE_VERSION = "1.0.0"


def activate(system):
    system.add_history("Modulo de teste carregado")
    system.memory["test_module_loaded"] = True
    return f"{MODULE_NAME} v{MODULE_VERSION} foi carregado com sucesso."
