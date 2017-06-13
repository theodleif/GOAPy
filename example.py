from goapy import Planner, Action_List

def print_path():
    global _world
    global _actions
    global _path
    for path in _path:
        print _path.index(path)+1, path['name']
        if path['name'] in _actions.changes:
            pn = path['name']
            ac = _actions.changes[pn]
            print "At",pn, "goal changes",ac
            for c in ac:
                _world.goal_state[c] = ac[c]
            del _actions.changes[path['name']]
            _path = _world.calculate()
            return False
    return True
    
if __name__ == '__main__':
    import time

    _world = Planner('hungry', 'has_food', 'in_kitchen', 'tired', 'in_bed', 'has_money',
                     'is_fat', 'has_ingredients')
    _world.set_start_state(hungry=True, has_food=False, in_kitchen=False, tired=True, in_bed=False, 
                           has_money=False, is_fat=False, has_ingredients=False)
    _world.set_goal_state(tired=False, is_fat=True)

    _actions = Action_List()
    _actions.add_condition('eat', hungry=True, has_food=True, in_kitchen=False)
    _actions.add_reaction('eat', hungry=False, has_food=False)
    _actions.add_condition('cook', hungry=True, has_food=False, in_kitchen=True, has_ingredients=True)
    _actions.add_reaction('cook', has_food=True, has_ingredients=False)
    _actions.add_condition('sleep', tired=True, in_bed=True)
    _actions.add_reaction('sleep', tired=False)
    _actions.add_condition('go_to_bed', in_bed=False, hungry=False)
    _actions.add_reaction('go_to_bed', in_bed=True)
    _actions.add_condition('go_to_kitchen', in_kitchen=False)
    _actions.add_reaction('go_to_kitchen', in_kitchen=True)
    _actions.add_condition('leave_kitchen', in_kitchen=True)
    _actions.add_reaction('leave_kitchen', in_kitchen=False)
    _actions.add_condition('order_pizza', has_food=False, hungry=True, has_money=True)
    _actions.add_reaction('order_pizza', has_food=True, is_fat=True, has_money=False) 
    _actions.add_condition('fetch_money', has_money=False)
    _actions.add_reaction('fetch_money', has_money=True)
    _actions.add_condition('buy_ingredients', has_money=True, in_kitchen=False)
    _actions.add_reaction('buy_ingredients', has_money=False, has_ingredients=True)
    _actions.set_weight('cook', 20)
    _actions.set_weight('order_pizza', 2)
    _actions.set_weight('fetch_money', 20)
    _actions.change_goal('order_pizza', is_fat=False)

    _world.set_action_list(_actions)
    
    _t = time.time()
    _path = _world.calculate()
    _took_time = time.time() - _t

    passflag = False

    while passflag==False:
        passflag = print_path()        
            

    print '\nTook:', _took_time
