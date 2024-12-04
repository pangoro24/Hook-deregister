import boto3

# Inicializar el cliente de CloudFormation
cfn_client = boto3.client("cloudformation")

def list_registered_hooks():
    """
    Obtiene una lista de todos los hooks registrados en la cuenta.
    """
    try:
        hooks = []
        paginator = cfn_client.get_paginator("list_types")
        
        for page in paginator.paginate(
            Filters={"Type": "HOOK"}
        ):
            for hook in page["TypeSummaries"]:
                hooks.append(hook["TypeName"])
        
        print(f"Se encontraron {len(hooks)} hooks registrados: {hooks}")
        return hooks

    except Exception as e:
        print(f"Error al listar hooks registrados: {e}")
        return []

def deregister_non_default_hook_versions(hook_name):
    """
    Desregistra todas las versiones activas no predeterminadas de un hook específico.
    """
    try:
        # Obtener todas las versiones del hook
        response = cfn_client.list_type_versions(
            Type="HOOK",
            TypeName=hook_name
        )

        # Filtrar versiones no predeterminadas que están activas
        non_default_active_versions = [
            version for version in response["TypeVersionSummaries"]
            if not version.get("IsDefaultVersion") and version.get("TypeVersionStatus") == "ACTIVE"
        ]

        # Iterar y desregistrar cada versión activa no predeterminada
        for version in non_default_active_versions:
            version_id = version["Arn"]
            print(f"Deregistrando versión: {version_id}")
            
            cfn_client.deregister_type(
                Arn=version_id
            )
            print(f"Versión {version_id} desregistrada con éxito.")
        
        print(f"Proceso completado para el hook: {hook_name}")
    except Exception as e:
        print(f"Error al desregistrar versiones del hook '{hook_name}': {e}")

def deregister_all_hooks():
    """
    Itera sobre todos los hooks registrados y desregistra sus versiones activas no predeterminadas.
    """
    hooks = list_registered_hooks()
    
    if not hooks:
        print("No hay hooks registrados para procesar.")
        return

    for hook_name in hooks:
        print(f"Procesando hook: {hook_name}")
        deregister_non_default_hook_versions(hook_name)

# Ejecutar la función principal
if __name__ == "__main__":
    deregister_all_hooks()
