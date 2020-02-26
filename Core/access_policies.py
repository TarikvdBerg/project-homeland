from rest_access_policy import AccessPolicy

class SCTFUserAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list"],
            "principal": ["group:admin"],
            "effect": "allow",
        },
        {
            "action": ["create"],
            "principal": ["anonymous", "group:admin"],
            "effect": "allow",
        },
        {
            "action": ["retrieve", "update", "destroy"],
            "principal": ["authenticated", "group:admin"],
            "effect": "allow",
        }
    ]

class PasswordGroupAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "create", "retrieve", "update", "destroy"],
            "principal": ["authenticated"],
            "effect": "allow"
        }
    ]

class PasswordAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "create", "retrieve", "update", "destroy"],
            "principal":["authenticated"],
            "effect": "allow"
        }
    ]