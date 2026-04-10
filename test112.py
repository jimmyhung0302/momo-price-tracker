def unrequitted_experience(lover):
    count = len(lover)
    
    print(f"你總共暈過{count}個女生")
    
    mixed_name="+".join(lover)

    return mixed_name
my_belove=["","","",""]
love=unrequitted_experience(my_belove)

print(love)