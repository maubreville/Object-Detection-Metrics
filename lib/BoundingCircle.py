from utils import *
"""
    Bounding Circle utils (from )

"""
# size => (width, height) of the image
# box => (X1, X2, Y1, Y2) of the bounding box
def convertCircleToRelativeValues(size, box):
    dr = 1. / (size[0])
    dh = 1. / (size[1])
    cx = box[0]
    cy = box[1]
    r = box[2]
    x = cx * dw
    y = cy * dh
    r = r * dw
    # x,y => (bounding_box_center)/width_of_the_image
    # w => bounding_box_width / width_of_the_image
    # h => bounding_box_height / height_of_the_image
    return (x, y, r)


# size => (width, height) of the image
# box => (centerX, centerY, w, h) of the bounding box relative to the image
def convertCircleToAbsoluteValues(size, box):
    # w_box = round(size[0] * box[2])
    # h_box = round(size[1] * box[3])
    xIn = round(((2 * float(box[0]) ) * size[0] / 2))
    yIn = round(((2 * float(box[1]) ) * size[1] / 2))
    rIn = round(((2 * float(box[2]) ) * size[0] / 2))
    if xIn < 0:
        xIn = 0
    if yIn < 0:
        yIn = 0
    
    return (xIn, yIn, rIn)

class BoundingCircle:
    def __init__(self,
                 imageName,
                 classId,
                 x,
                 y,
                 r,
                 typeCoordinates=CoordinatesType.Absolute,
                 imgSize=None,
                 bbType=BBType.GroundTruth,
                 classConfidence=None):
        """Constructor.
        Args:
            imageName: String representing the image name.
            classId: String value representing class id.
            x: Float value representing the X upper-left coordinate of the bounding circle.
            y: Float value representing the Y upper-left coordinate of the bounding circle.
            r: Float value representing the radius of the bounding circle.
            typeCoordinates: (optional) Enum (Relative or Absolute) represents if the bounding box
            coordinates (x,y,r) are absolute or relative to size of the image. Default:'Absolute'.
            imgSize: (optional) 2D vector (width, height)=>(int, int) represents the size of the
            image of the bounding box. If typeCoordinates is 'Relative', imgSize is required.
            bbType: (optional) Enum (Groundtruth or Detection) identifies if the bounding box
            represents a ground truth or a detection. If it is a detection, the classConfidence has
            to be informed.
            classConfidence: (optional) Float value representing the confidence of the detected
            class. If detectionType is Detection, classConfidence needs to be informed.
        """
        self._imageName = imageName
        self._typeCoordinates = typeCoordinates
        if typeCoordinates == CoordinatesType.Relative and imgSize is None:
            raise IOError(
                'Parameter \'imgSize\' is required. It is necessary to inform the image size.')
        if bbType == BBType.Detected and classConfidence is None:
            raise IOError(
                'For bbType=\'Detection\', it is necessary to inform the classConfidence value.')
        # if classConfidence != None and (classConfidence < 0 or classConfidence > 1):
        # raise IOError('classConfidence value must be a real value between 0 and 1. Value: %f' %
        # classConfidence)

        self._classConfidence = classConfidence
        self._bbType = bbType
        self._classId = classId
        self._format = format

        # If relative coordinates, convert to absolute values
        # For relative coords: (x,y,w,h)=(X_center/img_width , Y_center/img_height)
        if (typeCoordinates == CoordinatesType.Relative):
            (self._x, self._y, self._r) = convertCircleToAbsoluteValues(imgSize, (x, y, r))
            self._width_img = imgSize[0]
            self._height_img = imgSize[1]

            # For absolute coords: (x,y,w,h)=real bb coords
        else:
            self._x = x
            self._y = y
            self._r = r

        if imgSize is None:
            self._width_img = None
            self._height_img = None
        else:
            self._width_img = imgSize[0]
            self._height_img = imgSize[1]
 
    def getAbsoluteBoundingObject(self, format=BBFormat.XYWH):
            return (self._x, self._y, self._r)

    def getRelativeBoundingObject(self, imgSize=None):
        print('getRelBBOX triggered')
        if imgSize is None and self._width_img is None and self._height_img is None:
            raise IOError(
                'Parameter \'imgSize\' is required. It is necessary to inform the image size.')
        if imgSize is None:
            return convertCircleToRelativeValues((imgSize[0], imgSize[1]),
                                           (self._x, self._y, self._r))
        else:
            return convertToRelativeValues((self._width_img, self._height_img),
                                           (self._x, self._y, self.r))

    def getImageName(self):
        return self._imageName

    def getConfidence(self):
        return self._classConfidence

    def getFormat(self):
        return self._format

    def getClassId(self):
        return self._classId

    def getImageSize(self):
        return (self._width_img, self._height_img)

    def getCoordinatesType(self):
        return self._typeCoordinates

    def getBBType(self):
        return self._bbType

    @staticmethod
    def compare(det1, det2):
        det1BB = det1.getAbsoluteBoundingBox()
        det1ImgSize = det1.getImageSize()
        det2BB = det2.getAbsoluteBoundingBox()
        det2ImgSize = det2.getImageSize()

        if det1.getClassId() == det2.getClassId() and \
           det1.classConfidence == det2.classConfidenc() and \
               det1BB[0] == det2BB[0] and \
           det1BB[1] == det2BB[1] and \
           det1BB[2] == det2BB[2] and \
           det1BB[3] == det2BB[3] and \
           det1ImgSize[0] == det1ImgSize[0] and \
           det2ImgSize[1] == det2ImgSize[1]:
            return True
        return False

    @staticmethod
    def clone(boundingBox):
        absBB = boundingBox.getAbsoluteBoundingBox(format=BBFormat.XYWH)
        # return (self._x,self._y,self._x2,self._y2)
        newBoundingBox = BoundingBox(
            boundingBox.getImageName(),
            boundingBox.getClassId(),
            absBB[0],
            absBB[1],
            absBB[2],
            absBB[3],
            typeCoordinates=boundingBox.getCoordinatesType(),
            imgSize=boundingBox.getImageSize(),
            bbType=boundingBox.getBBType(),
            classConfidence=boundingBox.getConfidence(),
            format=BBFormat.XYWH)
        return newBoundingBox

