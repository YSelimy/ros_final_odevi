#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from pyzbar.pyzbar import decode, ZBarSymbol

class QRReader:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.callback)
        # SİHİRLİ DOKUNUŞ: Görev yöneticisine haber vermek için yayıncı açıyoruz
        self.qr_pub = rospy.Publisher('/detected_qr', String, queue_size=10)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            return

        # Sadece QR Kodları ara, diğer barkod tiplerini ve raf çizgilerini yoksay
        decoded_objects = decode(cv_image, symbols=[ZBarSymbol.QRCODE])
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            # Okunan veriyi beyne (task_manager) gönder
            self.qr_pub.publish(qr_data)
            
            points = obj.polygon
            if len(points) == 4:
                pts = [(p.x, p.y) for p in points]
                cv2.polylines(cv_image, [np.array(pts, dtype=np.int32)], True, (0, 255, 0), 3)

        cv2.imshow("TurtleBot3 Canli Kamera Paneli", cv_image)
        cv2.waitKey(3)

if __name__ == "__main__":
    rospy.init_node('qr_reader_node', anonymous=True)
    qr_reader = QRReader()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass
    cv2.destroyAllWindows()
