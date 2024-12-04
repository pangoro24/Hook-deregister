import boto3

# Inicializar el cliente de CloudFormation
cfn_client = boto3.client("cloudformation")

def deregister_non_default_hook_versions(hook_name):
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
        
        print("Proceso completado.")
    except Exception as e:
        print(f"Error al desregistrar versiones del hook: {e}")

# Nombre del hook
hook_name = "MyHookName"  # Cambia esto por el nombre de tu hook

# Ejecutar la función
deregister_non_default_hook_versions(hook_name)

