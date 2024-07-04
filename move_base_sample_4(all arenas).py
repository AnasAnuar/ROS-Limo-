#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus

# Define waypoints for different arenas
map_origin = [
    [(0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0)]
]
arena_1 = [
    [(-0.286, 0.0441, 0.0), (0.0, 0.0, -0.324, 0.945)]
]

arena_2a = [
    [(-0.206, -0.428, 0.0), (0.0, 0.0, 0.998, -0.058)]
]

arena_2b = [
    [(-0.206, -0.428, 0.0), (0.0, 0.0, 0.998, -0.058)]
]

arena_3a = [
    [(-0.714, -0.49, 0.0), (-0.0, 0.0, 0.995, -0.0919)]
]

arena_3b = [
    [(-0.734, -0.51, 0.0), (-0.0, 0.0, 0.995, -0.1019)]
]

arena_4a = [
    [(-1.66, -0.648, 0.0), (0.0, 0.0, -0.817, 0.576)]
]

arena_4b = [
    [(-1.68, -0.668, 0.0), (0.0, 0.0, -0.827, 0.586)]
]

arena_4c = [
    [(-1.68, -0.668, 0.0), (0.0, 0.0, -0.827, 0.586)]
]

arena_5 = [
    [(-1.027, -1.538, 0.0), (0.0, 0.0, -0.696, 0.717)]
]

arena_6a = [
    [(-0.662, -1.12, 0.0), (0.0, 0.0, 0.0977, 0.995)]
]

arena_6b = [
    [(-0.662, -1.12, 0.0), (0.0, 0.0, 0.0977, 0.995)]
]

arena_7 = [
    [(-0.231, -1.074, 0.0), (0.0, 0.0, 0.416, 0.909)]
]

arena_8a = [
    [(-0.5835, -0.309, 0.0), (0.0, 0.0, 0.76, 0.649)]
]

arena_8b = [
    [(-0.5835, -0.309, 0.0), (0.0, 0.0, 0.76, 0.649)]
]

def goal_pose(pose):
    goal_pose = MoveBaseGoal()
    goal_pose.target_pose.header.frame_id = 'map'
    goal_pose.target_pose.header.stamp = rospy.Time.now()
    goal_pose.target_pose.pose.position.x = pose[0][0]
    goal_pose.target_pose.pose.position.y = pose[0][1]
    goal_pose.target_pose.pose.position.z = pose[0][2]
    goal_pose.target_pose.pose.orientation.x = pose[1][0]
    goal_pose.target_pose.pose.orientation.y = pose[1][1]
    goal_pose.target_pose.pose.orientation.z = pose[1][2]
    goal_pose.target_pose.pose.orientation.w = pose[1][3]
    
    return goal_pose

if __name__ == '__main__':
    rospy.init_node('simple_client')
    
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    while True:
        # User selects the arena to use
        print("\nSelect arena (enter 0 to exit):")
        print("1. Arena 1")
        print("2. Arena 2a")
        print("3. Arena 2b")        #arena middle exit
        print("4. Arena 3a")
        print("5. Arena 3b")
        print("6. Arena 4a")
        print("7. Arena 4b")
        print("8. Arena 4c")        #arena middle exit
        print("9. Arena 5")
        print("10. Arena 6a")
        print("11. Arena 6b")       #arena middle exit
        print("12. Arena 7")
        print("13. Arena 8a")
        print("14. Arena 8b")       #arena middle exit
        print("15. map_origin")
        
        choice = int(input("Enter your choice of arena (0-10): "))
        
        if choice == 0:
            print("Exiting.")
            break
        elif choice == 1:
            selected_arena = arena_1
        elif choice == 2:
            selected_arena = arena_2a
        elif choice == 3:
            selected_arena = arena_2b
        elif choice == 4:
            selected_arena = arena_3a
        elif choice == 5:
            selected_arena = arena_3b
        elif choice == 6:
            selected_arena = arena_4a
        elif choice == 7:
            selected_arena = arena_4b
        elif choice == 8:
            selected_arena = arena_4c
        elif choice == 9:
            selected_arena = arena_5
        elif choice == 10:
            selected_arena = arena_6a
        elif choice == 11:
            selected_arena = arena_6b
        elif choice == 12:
            selected_arena = arena_7
        elif choice == 13:
            selected_arena = arena_8a
        elif choice == 14:
            selected_arena = arena_8b
        elif choice == 15:
            selected_arena = map_origin
        else:
            print("Invalid choice. Try again.")
            continue

        for pose in selected_arena:
            goal = goal_pose(pose)
            client.send_goal(goal)
            
            while not rospy.is_shutdown():
                state = client.get_state()
                if state == GoalStatus.SUCCEEDED:
                    print("Goal reached")
                    break
                elif state in [GoalStatus.ABORTED, GoalStatus.REJECTED, GoalStatus.PREEMPTED]:
                    print("Goal could not be reached")
                    break
                elif state == GoalStatus.ACTIVE:
                    # Implementing custom stuck detection
                    if client.get_goal_status_text() == "Oscillation detected":
                        print("Robot stuck due to oscillation")
                        break
                rospy.sleep(0.1)
