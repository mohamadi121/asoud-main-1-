"""
API Documentation Views
"""
from django.http import JsonResponse
from django.views import View
from rest_framework import views
from rest_framework.response import Response
from utils.response import ApiResponse


class APIEndpointsView(views.APIView):
    """
    Interactive API documentation endpoint
    """
    permission_classes = []  # Public access
    
    def get(self, request):
        """
        Returns comprehensive API documentation
        """
        api_docs = {
            "version": "1.8",
            "title": "ASOUD API Documentation",
            "description": "Complete marketplace API for multi-vendor e-commerce platform",
            "base_url": "https://asoud.ir/api/v1/",
            "authentication": {
                "type": "Token Authentication",
                "header": "Authorization: Token <your_token>",
                "obtain_token": "/api/v1/user/pin/verify/"
            },
            "endpoints": {
                "authentication": {
                    "pin_create": {
                        "url": "/api/v1/user/pin/create/",
                        "method": "POST",
                        "description": "Create PIN for mobile verification",
                        "parameters": {
                            "mobile_number": {"type": "string", "required": True, "format": "09XXXXXXXXX"}
                        },
                        "response_example": {
                            "success": True,
                            "code": 200,
                            "message": "PIN created successfully"
                        }
                    },
                    "pin_verify": {
                        "url": "/api/v1/user/pin/verify/",
                        "method": "POST",
                        "description": "Verify PIN and get authentication token",
                        "parameters": {
                            "mobile_number": {"type": "string", "required": True},
                            "pin": {"type": "string", "required": True, "format": "4 digits"}
                        },
                        "response_example": {
                            "success": True,
                            "code": 200,
                            "data": {"token": "auth_token_here"},
                            "message": "Authentication successful"
                        }
                    }
                },
                "market": {
                    "create_market": {
                        "url": "/api/v1/owner/market/create/",
                        "method": "POST",
                        "authentication_required": True,
                        "description": "Create new marketplace",
                        "parameters": {
                            "name": {"type": "string", "required": True},
                            "business_id": {"type": "string", "required": True, "pattern": "^[a-z0-9_-]{3,20}$"}
                        }
                    },
                    "list_markets": {
                        "url": "/api/v1/user/market/list/",
                        "method": "GET",
                        "description": "List all active markets",
                        "authentication_required": False
                    }
                },
                "admin_security": {
                    "security_status": {
                        "url": "/api/v1/secure-admin/security/status/",
                        "method": "GET",
                        "authentication_required": True,
                        "permission": "superuser_only",
                        "description": "Admin security status and session validation"
                    },
                    "dashboard_stats": {
                        "url": "/api/v1/secure-admin/dashboard/stats/",
                        "method": "GET",
                        "authentication_required": True,
                        "permission": "superuser_only",
                        "description": "Comprehensive admin dashboard statistics"
                    },
                    "users_list": {
                        "url": "/api/v1/secure-admin/users/",
                        "method": "GET",
                        "authentication_required": True,
                        "permission": "superuser_only",
                        "description": "List all users with advanced filtering",
                        "parameters": {
                            "page": "Page number (default: 1)",
                            "limit": "Items per page (max: 100, default: 50)",
                            "search": "Search in mobile, first_name, last_name",
                            "type": "Filter by user type (USER, OWNER, MARKETER)",
                            "active": "Filter by active status (true/false)"
                        }
                    },
                    "user_detail": {
                        "url": "/api/v1/secure-admin/users/{user_id}/",
                        "method": "GET",
                        "authentication_required": True,
                        "permission": "superuser_only",
                        "description": "Get detailed user information"
                    },
                    "user_toggle_active": {
                        "url": "/api/v1/secure-admin/users/{user_id}/toggle-active/",
                        "method": "PATCH",
                        "authentication_required": True,
                        "permission": "superuser_only",
                        "description": "Activate/deactivate user account"
                    },
                    "system_health": {
                        "url": "/api/v1/secure-admin/system/health/",
                        "method": "GET",
                        "authentication_required": True,
                        "permission": "superuser_only",
                        "description": "System health check and monitoring"
                    },
                    "audit_logs": {
                        "url": "/api/v1/secure-admin/audit/logs/",
                        "method": "GET",
                        "authentication_required": True,
                        "permission": "superuser_only",
                        "description": "View admin audit logs"
                    }
                },
                "user_management": {
                    "register": {
                        "url": "/api/v1/user/register/",
                        "method": "POST",
                        "authentication_required": False,
                        "description": "User registration with mobile number",
                        "parameters": {
                            "mobile_number": "User mobile number (required)",
                            "type": "User type: USER, OWNER, MARKETER (default: USER)"
                        }
                    },
                    "verify_pin": {
                        "url": "/api/v1/user/verify-pin/",
                        "method": "POST",
                        "authentication_required": False,
                        "description": "Verify PIN and get authentication token",
                        "parameters": {
                            "mobile_number": "User mobile number",
                            "pin": "Verification PIN"
                        }
                    },
                    "profile": {
                        "url": "/api/v1/user/profile/",
                        "method": "GET",
                        "authentication_required": True,
                        "description": "Get user profile information"
                    },
                    "update_profile": {
                        "url": "/api/v1/user/profile/update/",
                        "method": "PATCH",
                        "authentication_required": True,
                        "description": "Update user profile information"
                    }
                },
                "market_management": {
                    "create_market": {
                        "url": "/api/v1/owner/market/create/",
                        "method": "POST",
                        "authentication_required": True,
                        "permission": "owner_or_marketer",
                        "description": "Create new market/shop",
                        "parameters": {
                            "name": "Market name (required)",
                            "type": "Market type: company, shop",
                            "business_id": "Unique business identifier for subdomain",
                            "description": "Market description"
                        }
                    },
                    "list_markets": {
                        "url": "/api/v1/owner/market/list/",
                        "method": "GET",
                        "authentication_required": True,
                        "permission": "owner_or_marketer",
                        "description": "List user's markets"
                    },
                    "market_detail": {
                        "url": "/api/v1/owner/market/{market_id}/",
                        "method": "GET",
                        "authentication_required": True,
                        "permission": "owner_or_marketer",
                        "description": "Get market details"
                    },
                    "update_market": {
                        "url": "/api/v1/owner/market/update/{market_id}/",
                        "method": "PATCH",
                        "authentication_required": True,
                        "permission": "owner_or_marketer",
                        "description": "Update market information"
                    },
                    "publish_market": {
                        "url": "/api/v1/owner/market/queue/{market_id}/",
                        "method": "POST",
                        "authentication_required": True,
                        "permission": "owner_or_marketer",
                        "description": "Submit market for publication review"
                    }
                },
                "product_management": {
                    "create_product": {
                        "url": "/api/v1/owner/product/create/",
                        "method": "POST",
                        "authentication_required": True,
                        "permission": "owner_or_marketer",
                        "description": "Add new product to marketplace",
                        "parameters": {
                            "market": "Market ID (required)",
                            "name": "Product name (required)",
                            "type": "Product type: good, service",
                            "description": "Product description",
                            "price": "Product price",
                            "stock": "Available stock quantity"
                        }
                    },
                    "list_products": {
                        "url": "/api/v1/owner/product/list/{market_id}/",
                        "method": "GET",
                        "authentication_required": True,
                        "permission": "owner_or_marketer",
                        "description": "List products for specific market"
                    },
                    "product_detail": {
                        "url": "/api/v1/owner/product/detail/{product_id}/",
                        "method": "GET",
                        "authentication_required": True,
                        "permission": "owner_or_marketer",
                        "description": "Get product details"
                    },
                    "public_products": {
                        "url": "/api/v1/user/product/list/",
                        "method": "GET",
                        "authentication_required": False,
                        "description": "List public products with filtering",
                        "parameters": {
                            "category": "Filter by category ID",
                            "market": "Filter by market ID",
                            "search": "Search in product name and description",
                            "min_price": "Minimum price filter",
                            "max_price": "Maximum price filter"
                        }
                    }
                },
                "payment_system": {
                    "create_payment": {
                        "url": "/api/v1/user/payments/create/",
                        "method": "POST",
                        "authentication_required": True,
                        "description": "Initiate payment process",
                        "parameters": {
                            "amount": "Payment amount (required)",
                            "target_type": "Target content type",
                            "target_id": "Target object ID",
                            "gateway": "Payment gateway (zarinpal)"
                        }
                    },
                    "payment_verify": {
                        "url": "/api/v1/user/payments/verify/",
                        "method": "POST",
                        "authentication_required": True,
                        "description": "Verify payment status",
                        "parameters": {
                            "authority": "Payment authority from gateway",
                            "status": "Payment status from gateway"
                        }
                    },
                    "payment_history": {
                        "url": "/api/v1/user/payments/history/",
                        "method": "GET",
                        "authentication_required": True,
                        "description": "Get user payment history"
                    }
                },
                "chat_system": {
                    "websocket_url": "wss://asoud.ir/api/v1/user/chat/",
                    "description": "Real-time chat WebSocket connection",
                    "authentication_required": True,
                    "connection_info": {
                        "protocol": "WebSocket",
                        "authentication": "Token in query string: ?token=your_auth_token",
                        "message_format": "JSON"
                    },
                    "message_types": {
                        "send_message": {
                            "type": "chat_message",
                            "data": {
                                "conversation_id": "Conversation UUID",
                                "message": "Text message",
                                "file": "Optional file data"
                            }
                        },
                        "join_conversation": {
                            "type": "join_conversation",
                            "data": {
                                "conversation_id": "Conversation UUID"
                            }
                        }
                    }
                },
                "wallet_system": {
                    "balance": {
                        "url": "/api/v1/wallet/balance/",
                        "method": "GET",
                        "authentication_required": True,
                        "description": "Get wallet balance"
                    },
                    "charge_wallet": {
                        "url": "/api/v1/wallet/charge/",
                        "method": "POST",
                        "authentication_required": True,
                        "description": "Charge wallet with payment",
                        "parameters": {
                            "amount": "Charge amount (required)"
                        }
                    },
                    "transactions": {
                        "url": "/api/v1/wallet/transactions/",
                        "method": "GET",
                        "authentication_required": True,
                        "description": "Get wallet transaction history"
                    }
                },
                "category_system": {
                    "list_groups": {
                        "url": "/api/v1/category/group/list/",
                        "method": "GET",
                        "authentication_required": False,
                        "description": "List all category groups"
                    },
                    "list_categories": {
                        "url": "/api/v1/category/list/{group_id}/",
                        "method": "GET",
                        "authentication_required": False,
                        "description": "List categories in a group"
                    },
                    "list_subcategories": {
                        "url": "/api/v1/category/sub/list/{category_id}/",
                        "method": "GET",
                        "authentication_required": False,
                        "description": "List subcategories"
                    }
                },
                "reservation_system": {
                    "list_services": {
                        "url": "/api/v1/reservation/user/service/",
                        "method": "GET",
                        "authentication_required": False,
                        "description": "List available services for reservation"
                    },
                    "create_reservation": {
                        "url": "/api/v1/reservation/user/reservation/create/",
                        "method": "POST",
                        "authentication_required": True,
                        "description": "Create new service reservation",
                        "parameters": {
                            "service_id": "Service ID (required)",
                            "specialist_id": "Specialist ID (optional)",
                            "date": "Reservation date",
                            "time": "Reservation time"
                        }
                    },
                    "reservation_list": {
                        "url": "/api/v1/reservation/user/reservation/",
                        "method": "GET",
                        "authentication_required": True,
                        "description": "List user reservations"
                    }
                }
            },
            "error_codes": {
                "400": "validation_error - Request validation failed",
                "401": "authentication_required - Authentication required", 
                "403": "permission_denied - Access forbidden",
                "404": "not_found - Resource not found",
                "429": "rate_limit_exceeded - Rate limit exceeded",
                "500": "server_error - Server error occurred"
            },
            "rate_limits": {
                "anonymous": "50 requests per hour",
                "authenticated": "500 requests per hour",
                "pin_create": "5 requests per hour",
                "payment": "10 requests per hour"
            },
            "data_formats": {
                "mobile_number": "Iranian format: 09XXXXXXXXX",
                "pin": "4 digits: 1234",
                "business_id": "3-20 characters, alphanumeric with dash/underscore",
                "amount": "Decimal format, minimum 0.01, maximum 999999999999.99"
            }
        }
        
        return Response(ApiResponse(
            success=True,
            code=200,
            data=api_docs,
            message="API documentation retrieved"
        ))


class HealthCheckView(View):
    """
    Simple health check endpoint for monitoring
    """
    def get(self, request):
        return JsonResponse({
            "status": "healthy",
            "version": "1.8",
            "timestamp": "2025-07-24T11:00:00Z"
        })