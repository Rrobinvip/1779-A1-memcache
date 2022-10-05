# ECE 1779 A1 MEMCACHE - Group 17

## To create environment:
1. Create the environment from the `environment.yml`
`conda env create -f environment.yml`
2. Activate the new environment, in this case, the `<name_env>` is `MEMCACHE`
`conda activate <name_env>`
3. Inspect packages
`conda list`

## To run:
1. At base dir
`python3 run.py`

## 5 key components:
1. The web browser that initiates requests
2. The web front end that manages requests and operations
3. The local file system where all data is stored
4. The mem-cache that provides faster access
5. The relational database (RDBMS), which stores a list of known keys, the configuration parameters, and other important values.

## To do list
### P1 Front end 
1. ~~A page to upload a new pair of key and image~~
2. A page that shows an image associated with a given key
3. ~~A page that displays all the available keys stored in the database~~
4. A page to configure the mem-cache parameters (e.g., capacity in MB, replacement policy) as well as clear the cache. 
5. Display a page with the current statistics for the mem-cache over the past 10 minutes
6. Key-Value memcache, see below for details

### P2 Key-value memcache
1. `PUT(key, value)` to set the key and value (contents of the image)
2. `GET(key)` to get the content associated with the key
3. `CLEAR()` to drop all keys and values
4. `invalidateKey(key)` to drop a specific key
5. `refreshConfiguration()` to read mem-cache related details from the database and reconfigure it based on the values set by the user (see 4. above)

### P3 mem-cache cache replacement policies
1. Random Replacement: Randomly selects a key and discards it to make space when necessary. This algorithm does not require keeping any information about the access history.
2. Least Recently Used: Discards the least recently used keys first. This algorithm requires keeping track of what was used when, if one wants to make sure the algorithm always discards the least recently used key.

### Other requirements
1. P1.1, the key should be used to uniquely identify its image. A subsequent upload with the same key will replace the image stored previously. The web front end should store the image in the local file system, and add the key to the list of known keys in the database. Upon an update, the mem-cache entry with this key should be invalidated.
2. Configuration parameters and statistic of memcache needs to be stored in DB.
3. Memcache needs to update its status every 5 sec.
4. API for access and testing. 

**Still editing..**
