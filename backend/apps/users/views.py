from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from apps.products.models import Product
from .models import Cart, CartItem
from .serializers import RegisterSerializer, LoginSerializer, CartSerializer


class RegisterView(generics.CreateAPIView):
    """
    API đăng ký tài khoản mới.
    Cho phép tất cả mọi người truy cập, không cần xác thực.
    POST /api/auth/register/
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Tạo tài khoản mới và trả về thông báo thành công."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'Đăng ký thành công',
            'email': user.email
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    API đăng nhập tài khoản.
    Trả về access_token và refresh_token nếu đăng nhập thành công.
    POST /api/auth/login/
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """Xác thực thông tin đăng nhập và trả về JWT token."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Đăng nhập thành công',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role,
            }
        }, status=status.HTTP_200_OK)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    def get(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        try:
            quantity = int(request.data.get('quantity', 1))
        except (TypeError, ValueError):
            return Response({'error': 'So luong khong hop le.'}, status=status.HTTP_400_BAD_REQUEST)

        if quantity < 1:
            return Response({'error': 'So luong phai lon hon 0.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id, business_status='active')
        except Product.DoesNotExist:
            return Response({'error': 'San pham khong ton tai hoac khong dang ban.'}, status=status.HTTP_404_NOT_FOUND)

        if product.stock_quantity < quantity:
            return Response({'error': 'So luong ton kho khong du.'}, status=status.HTTP_400_BAD_REQUEST)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            next_quantity = item.quantity + quantity
            if product.stock_quantity < next_quantity:
                return Response({'error': 'So luong ton kho khong du.'}, status=status.HTTP_400_BAD_REQUEST)
            item.quantity = next_quantity
            item.save()

        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        try:
            quantity = int(request.data.get('quantity', 1))
        except (TypeError, ValueError):
            return Response({'error': 'So luong khong hop le.'}, status=status.HTTP_400_BAD_REQUEST)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        try:
            item = cart.items.select_related('product').get(id=item_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'San pham khong co trong gio hang.'}, status=status.HTTP_404_NOT_FOUND)

        if quantity <= 0:
            item.delete()
        else:
            if item.product.stock_quantity < quantity:
                return Response({'error': 'So luong ton kho khong du.'}, status=status.HTTP_400_BAD_REQUEST)
            item.quantity = quantity
            item.save()

        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.filter(id=item_id).delete()
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
