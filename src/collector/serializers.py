from rest_framework import serializers
import hashlib
from . import models

class TranscriptionDataSerializer(serializers.ModelSerializer):
    datahash = serializers.SerializerMethodField('get_data_hash')

    class Meta:
        model = models.TranscriptionData
        fields = [
            'puzzlePiece', 'bad_image', 'orientation', 'center',
            'wall1', 'wall2', 'wall3', 'wall4', 'wall5', 'wall6',
            'link1', 'link2', 'link3', 'link4', 'link5', 'link6',
            'datahash'
        ]

    def get_data_hash(self, transcription):
        hashStr = transcription.center + ' ' + \
                  str(1 if transcription.wall1 else 0) + \
                  str(1 if transcription.wall2 else 0) + \
                  str(1 if transcription.wall3 else 0) + \
                  str(1 if transcription.wall4 else 0) + \
                  str(1 if transcription.wall5 else 0) + \
                  str(1 if transcription.wall6 else 0) + \
                  ' ' + \
                  transcription.link1.strip() + ' ' + \
                  transcription.link2.strip() + ' ' + \
                  transcription.link3.strip() + ' ' + \
                  transcription.link4.strip() + ' ' + \
                  transcription.link5.strip() + ' ' + \
                  transcription.link6.strip()

        return hashlib.sha256(hashStr.upper().encode("utf-8")).hexdigest()


class PuzzlePieceSerializer(serializers.ModelSerializer):
    badimages = serializers.SerializerMethodField(read_only=True)
    isImage = serializers.SerializerMethodField('check_if_image')

    class Meta:
        model = models.PuzzlePiece
        fields = [
            'id', 'url', 'approved',
            'confidences', 'confidentsolutions',
            'badimages', 'rotatedimages',
            'transCount', 'isImage'
        ]

    def get_badimages(self, piece):
        # check if queryset was annotated
        if hasattr(piece, 'badimage_count'):
            return piece.badimage_count

        # queryset wasn't annotated, do the slow thing
        if piece.badimages.count() > 0:
            return piece.badimages.first().badCount

        return 0
    
    def check_if_image(self, instance):
        normalised_url = instance.url.lower()
        # Very naïve check for direct image links.
        # If extending this, be _very_ careful about complexity, because
        # this computation is done on GET request for each PuzzlePiece
        # individually.
        if normalised_url.endswith(".jpg") or normalised_url.endswith(".png") or normalised_url.endswith(".jpeg"):
            return True
        return False


class BadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BadImage
        fields = ['puzzlePiece', 'badCount']


class ConfidentSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PuzzlePiece
        fields = ['url', 'approved']
