from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from event.models import Event, EventType
from event.serializers import EventSerializer, EventTypeSerializer


class EventList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(instance=events, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.data.get('user')
        event_type = request.data.get('type')

        if user is None or event_type is None:
            return Response({'Required data were not provided'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventListDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(instance=event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(data=event)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventTypeList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        event_types = EventType.objects.all()
        serializer = EventTypeSerializer(data=event_types, many=True)
        return Response(serializer.data)
