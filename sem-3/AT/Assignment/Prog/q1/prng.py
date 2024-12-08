def solve():
    n,m,s,x = map(int, input().split())
    transition = [-1] * (n+1)
    for i in range (m):
        ai, bi = map(int, input().split())
        transition[ai] = bi
    
    
    freq = [0] * (n+1)
    current = s
    visited = [0] * (n+1)
    checker = False
    looplength = 0
    
    for i in range(1,x+1):   
        if(transition[current] == -1):
            checker = True
            return -1
        
        
        if(visited[current]):
            looplength = i - visited[current]
            break
        
        else :
            freq[current] += 1
            visited[current] = i
            current = transition[current]
    
    if checker:
        print("-1")
        return
    
    already = current
      
    if looplength != 0:
        while i <= x:
            freq[current] += ((x-i)//looplength) + 1
            current = transition[current]
            i += 1
            if current == already:
                break

    
        
    for i in range(1, n+1):
        print(freq[i], end=" ")
         
    print()
    

def main():
    # print("Hello World!")
    t = int(input())
    for _ in range(t):
        if(solve() == -1):
            print("-1")
            continue
        

if __name__ == "__main__":
    main()
    