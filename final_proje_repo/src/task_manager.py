#!/usr/bin/env python3
import rospy
import yaml
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import String

class TaskManager:
    def __init__(self):
        rospy.init_node('task_manager_node')
        self.latest_qr = None
        rospy.Subscriber('/detected_qr', String, self.qr_callback)
        
        with open('/home/ys/final_ws/src/config/mission.yaml', 'r') as file:
            self.mission_data = yaml.safe_load(file)

    def qr_callback(self, msg):
        self.latest_qr = msg.data

    def go_to_goal(self, x, y, qz, qw):
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        client.wait_for_server()

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.z = qz
        goal.target_pose.pose.orientation.w = qw

        client.send_goal(goal)
        wait = client.wait_for_result(rospy.Duration(90.0))
        if not wait:
            client.cancel_goal()
            return False
        return True

    def run_mission(self):
        locations = self.mission_data['locations']

        for loc in locations:
            rospy.loginfo(f"--- Yeni Hedef: {loc} ---")
            goal_data = self.mission_data[loc]['goal']
            expected_qr = self.mission_data[loc]['qr_expected']
            
            success = self.go_to_goal(goal_data['x'], goal_data['y'], goal_data['qz'], goal_data['qw'])
            
            if success:
                self.latest_qr = None
                qr_matched = False
                
                for attempt in range(3): 
                    rospy.sleep(2.0) 
                    
                    if self.latest_qr:
                        cleaned_qr = self.latest_qr.strip()
                        
                        if expected_qr in cleaned_qr:
                            rospy.loginfo(f"Gorev noktasi dogrulandi! Okunan: {cleaned_qr}")
                            qr_matched = True
                            break
                        else:
                            rospy.logwarn(f"Yanlis Tabela (Okunan: {cleaned_qr}, Beklenen: {expected_qr}). (Deneme {attempt+1}/3)")
                    else:
                        rospy.logwarn(f"Henuz bir QR okunamadi (Deneme {attempt+1}/3). Tekrar deneniyor...")
                
                if not qr_matched:
                    rospy.logerr(f"Gorev noktasi ATLANDI: {loc}")
                    
            else:
                rospy.logerr(f"Gorev noktasina ulasilamadi, ATLANDI: {loc}")
            
            self.latest_qr = None

if __name__ == "__main__":
    try:
        manager = TaskManager()
        manager.run_mission()
    except rospy.ROSInterruptException:
        pass
