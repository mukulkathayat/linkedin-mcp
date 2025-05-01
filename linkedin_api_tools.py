from mcp.server.fastmcp import FastMCP
from typing import List, Dict
import http.client
import json
import os
import urllib.parse

# Create MCP server
mcp = FastMCP("LinkedInProfiler")

# Get LinkedIn API credentials from environment variables
LINKEDIN_API_KEY = os.environ.get("LINKEDIN_API_KEY", "")
LINKEDIN_API_HOST = os.environ.get("LINKEDIN_API_HOST", "")
LINKEDIN_API_USER = os.environ.get("LINKEDIN_API_USER", "")

# LinkedIn API headers
LINKEDIN_HEADERS = {
    "Content-Type": "application/json",
    "x-rapidapi-host": LINKEDIN_API_HOST,
    "x-rapidapi-key": LINKEDIN_API_KEY,
    "x-rapidapi-user": LINKEDIN_API_USER
}

# LinkedIn API Tools based on api_doc.md

# Tool: Get Profiles
@mcp.tool()
def profiles(links: List[str]) -> Dict:
    """Can scrape up to 100 profiles data in a go
    
    Request Body Example:
    {
        "links": [
            "http://www.linkedin.com/in/luke-sharp-b3838719a",
            "http://www.linkedin.com/in/hollie-smith-96ab44b5"
        ]
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"links": links})
    conn.request("POST", "/profiles", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Get Companies
@mcp.tool()
def companies(links: List[str]) -> Dict:
    """Can scrape up to 100 companies data in a go
    
    Request Body Example:
    {
        "links": [
            "https://www.linkedin.com/company/huzzle-app/",
            "http://www.linkedin.com/company/aep-energy"
        ],
        "count": 1
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"links": links})
    conn.request("POST", "/companies", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Get Company Posts
@mcp.tool()
def company_posts(links: List[str], count: int = 1) -> Dict:
    """Can scrape 100 posts of 50 linkedin companies
    
    Request Body Example:
    {
        "links": [
            "https://www.linkedin.com/company/huzzle-app/",
            "http://www.linkedin.com/company/aep-energy"
        ],
        "count": 1
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"links": links, "count": count})
    conn.request("POST", "/company_posts", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Get Person Data
@mcp.tool()
def person(link: str) -> Dict:
    """Scrapes all data of a person from linkedin
    
    Request Body Example:
    {
        "link": "https://www.linkedin.com/in/ingmar-klein"
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"link": link})
    conn.request("POST", "/person", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Get Person Data Using URN
@mcp.tool()
def person_urn(link: str) -> Dict:
    """Scrapes all data from a person's page using his profile URN
    
    NOTE: This tool failed during testing (status 400, error: Failed to scrape profile).
    The API documentation is unclear if this expects a URN string or a full profile link with URN.

    Request Body Example:
    {
        "link": "https://www.linkedin.com/in/ACoAACeIPPkBUymOGNvgfbBL_uhKc32Hg_g_haU" 
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"link": link})
    conn.request("POST", "/person_urn", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Get Person Skills
@mcp.tool()
def person_skills(link: str) -> Dict:
    """Scrapes all skills of a linkedin user
    
    Request Body Example:
    {
        "link": "https://www.linkedin.com/in/ingmar-klein"
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"link": link})
    conn.request("POST", "/person_skills", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Search People With Filters
@mcp.tool()
def search_people_with_filters(keyword: str, page: int = 1, title_free_text: str = None, 
                            company_free_text: str = None, first_name: str = None, 
                            last_name: str = None) -> Dict:
    """Search for people from linkedin using all filters as per linkedin
    
    Request Body Example:
    {
        "keyword": "ingmar", 
        "page": 1, 
        "title_free_text": "CEO", 
        "company_free_text": "Huzzle", 
        "first_name": "Ingmar", 
        "last_name": "Klein"
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = {"keyword": keyword, "page": page}
    
    if title_free_text:
        payload["title_free_text"] = title_free_text
    if company_free_text:
        payload["company_free_text"] = company_free_text
    if first_name:
        payload["first_name"] = first_name
    if last_name:
        payload["last_name"] = last_name
        
    conn.request("POST", "/search_people_with_filters", json.dumps(payload), LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Get Company Data
@mcp.tool()
def company(link: str) -> Dict:
    """Scrapes all data from a provided company url
    
    Request Body Example:
    {
        "link": "https://www.linkedin.com/company/huzzle-app"
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"link": link})
    conn.request("POST", "/company", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Get Company Jobs
@mcp.tool()
def company_jobs(company_url: str, starts_from: int = 0, count: int = 10) -> Dict:
    """Scrapes jobs of a specific linkedin company
    
    Request Body Example:
    {
        "company_url": "https://www.linkedin.com/company/google",
        "starts_from": 0,
        "count": 10
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({
        "company_url": company_url,
        "starts_from": starts_from,
        "count": count
    })
    conn.request("POST", "/company_jobs", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Search Companies With Filters
@mcp.tool()
def search_company_with_filters(keyword: str, page: int = 1, company_size_list: str = None, 
                             hasJobs: bool = False, location_list: str = None, 
                             industry_list: str = None) -> Dict:
    """Search for companies as per linkedin search engine
    
    Request Body Example:
    {
        "keyword": "G", 
        "page": 1, 
        "company_size_list": "A,D", 
        "hasJobs": false, 
        "location_list": "", 
        "industry_list": ""
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = {"keyword": keyword, "page": page, "hasJobs": hasJobs}
    
    if company_size_list:
        payload["company_size_list"] = company_size_list
    if location_list:
        payload["location_list"] = location_list
    if industry_list:
        payload["industry_list"] = industry_list
        
    conn.request("POST", "/search_company_with_filters", json.dumps(payload), LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Get Post Data
@mcp.tool()
def post(link: str) -> Dict:
    """Scrapes post data by a person/company using its linkedin url
    
    Request Body Example:
    {
        "link": "https://www.linkedin.com/feed/update/urn:li:activity:7219434359085252608"
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"link": link})
    conn.request("POST", "/post", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Search Posts
@mcp.tool()
def search_posts(query: str, page: int = 1, filters: List[Dict] = None) -> Dict:
    """Search posts as per linkedin.com search engine (with filters)
    
    Request Body Example:
    {
        "page": 1,
        "query": "Top 10",
        "filters": [
            {
                "key": "datePosted",
                "values": "past-week"
            }
        ]
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = {"query": query, "page": page}
    
    if filters:
        payload["filters"] = filters
        
    conn.request("POST", "/search_posts", json.dumps(payload), LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Person Updates
@mcp.tool()
def profile_updates(profile_url: str, page: int = 1, paginationToken: str = None) -> Dict:
    """Scrapes updates posted by a linkedin user

    NOTE: API doc specifies profile_url and page as required GET parameters.
    
    Get Request Parameters:
    - profile_url: LinkedIn profile URL (paramType: STRING, required) (e.g., "http://www.linkedin.com/in/ingmar-klein")
    - page: Page number (paramType: NUMBER, required) (e.g., 1)
    - paginationToken: For pagination (paramType: STRING, optional)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    
    params = {"profile_url": profile_url, "page": page}
    if paginationToken:
        params["paginationToken"] = paginationToken

    # Construct query string with URL encoding
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    
    conn.request("GET", f"/profile_updates?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Person comments from recent activity
@mcp.tool()
def comments_from_recent_activity(profile_url: str, page: int = 1, paginationToken: str = None) -> Dict:
    """Scrapes comments posted by a person as per his recent activity

    NOTE: API doc specifies profile_url and page as required GET parameters.
    
    Get Request Parameters:
    - profile_url: LinkedIn profile URL (paramType: STRING, required) (e.g., "http://www.linkedin.com/in/ingmar-klein")
    - page: Page number (paramType: NUMBER, required) (e.g., 1)
    - paginationToken: For pagination (paramType: STRING, optional)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    
    params = {"profile_url": profile_url, "page": page}
    if paginationToken:
        params["paginationToken"] = paginationToken
        
    # Construct query string with URL encoding
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])

    conn.request("GET", f"/comments_from_recent_activity?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Company Updates
@mcp.tool()
def company_updates(company_url: str, page: str = "1", paginationToken: str = None) -> Dict:
    """Scrapes updates of a given company

    NOTE: API doc specifies company_url and page as required GET parameters.
    
    Get Request Parameters:
    - company_url: LinkedIn company URL (paramType: STRING, required) (e.g., "https://www.linkedin.com/company/google")
    - page: Page number (paramType: STRING, required) (e.g., "1")
    - paginationToken: For pagination (paramType: STRING, optional)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    
    params = {"company_url": company_url, "page": page}
    if paginationToken:
        params["paginationToken"] = paginationToken
        
    # Construct query string with URL encoding
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    
    conn.request("GET", f"/company_updates?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Company Employee Count
@mcp.tool()
def company_employee_count_per_skill(keyword: str, company_url: str) -> Dict:
    """Get employee count with specific skill at a company

    NOTE: API doc example uses camelCase 'companyUrl' in the request body.
    
    Request Body Example:
    {
        "keyword": "java",
        "companyUrl": "https://www.linkedin.com/company/google"
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"keyword": keyword, "companyUrl": company_url}) # Use camelCase for API
    conn.request("POST", "/company_employee_count_per_skill", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: School Alumni Count
@mcp.tool()
def school_alumini_count_per_skill(keyword: str, schoolUrl: str, skillExplicits: str = None) -> Dict:
    """Returns alumni count of a school/university

    NOTE: API doc example uses camelCase 'schoolUrl' in the request body.
    NOTE: This tool failed during testing with 400 Bad Request.
    
    Request Body Example:
    {
        "keyword": "",
        "schoolUrl": "https://www.linkedin.com/school/abertay-university",
        "skillExplicits": "260"
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload_dict = {"keyword": keyword, "schoolUrl": schoolUrl} # Use camelCase for API
    if skillExplicits:
        payload_dict["skillExplicits"] = skillExplicits
    payload = json.dumps(payload_dict)
    conn.request("POST", "/school_alumini_count_per_skill", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Company Employee
@mcp.tool()
def company_employee(company_id: str, page: int = 1) -> Dict:
    """Scrapes 12 people from a company (People Tab)

    NOTE: API doc specifies company_id and page as required GET parameters.
    NOTE: This tool failed persistently during testing (status 400, error: Couldn't recognize the parameter keys provided), unable to recognize parameters even when matching doc.
    
    Get Request Parameters:
    - company_id: LinkedIn company ID (paramType: STRING, required) (e.g., "1441" for Google)
    - page: Page number (paramType: NUMBER, required) (e.g., 1)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"companyId": company_id, "page": page}
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/company_employee?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Post Reactions
@mcp.tool()
def post_reactions(reactions_urn: str, pagination_token: str = None) -> Dict:
    """Data of the people who reacted to a particular post

    NOTE: Obtain 'reactionsUrn' from 'Company Updates' or 'Profile Updates' endpoints.
    
    Get Request Parameters:
    - reactionsUrn: URN for the post reactions (paramType: STRING, required) (e.g., "urn:li:activity:7219434359085252608/reactions")
    - paginationToken: For pagination (paramType: STRING, optional)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"reactions_urn": reactions_urn}
    if pagination_token:
        params["pagination_token"] = pagination_token
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/post_reactions?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Post Comments
@mcp.tool()
def post_comments(comments_urn: str, pagination_token: str = None) -> Dict:
    """Scrapes all commenters data who commented below a post

    NOTE: Obtain 'commentsUrn' from 'Company Updates' or 'Profile Updates' endpoints.

    Get Request Parameters:
    - commentsUrn: URN for the post comments (paramType: STRING, required) (e.g., "urn:li:activity:7219434359085252608/comments")
    - paginationToken: For pagination (paramType: STRING, optional)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"comments_urn": comments_urn}
    if pagination_token:
        params["pagination_token"] = pagination_token
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/post_comments?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Post Reposts
@mcp.tool()
def post_reposts(reposts_urn: str, pagination_token: str = None) -> Dict:
    """Scrapes all Reposters data who reposted a post

    NOTE: Obtain 'repostsUrn' from 'Company Updates' or 'Profile Updates' endpoints.
    
    Get Request Parameters:
    - repostsUrn: URN for the post reposts (paramType: STRING, required) (e.g., "urn:li:activity:7219434359085252608/reposts")
    - paginationToken: For pagination (paramType: STRING, optional)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"reposts_urn": reposts_urn}
    if pagination_token:
        params["pagination_token"] = pagination_token
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/post_reposts?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Search Posts With Filters
@mcp.tool()
def search_posts_with_filters(query: str = None, sort_by: str = None, from_member: str = None, 
                              from_organization: str = None, author_job_title: str = None,
                              author_company: str = None, content_type: str = None,
                              mentions_organization: str = None, author_industry: str = None,
                              mentions_member: str = None, page: str = "1") -> Dict:
    """Search for posts as per linkedin using all the available filters

    NOTE: API doc shows this endpoint uses different parameter names than previously implemented.
    
    Get Request Parameters:
    - query: Search term (paramType: STRING, optional) (e.g., "Top 10")
    - sort_by: Sorting option (paramType: STRING, optional)
    - from_member: Filter by member (paramType: STRING, optional)
    - from_organization: Filter by organization (paramType: STRING, optional)
    - author_job_title: Filter by author's job title (paramType: STRING, optional)
    - author_company: Filter by author's company (paramType: STRING, optional)
    - content_type: Filter by content type (paramType: STRING, optional)
    - mentions_organization: Filter by mentioned organization (paramType: STRING, optional)
    - author_industry: Filter by author's industry (paramType: STRING, optional)
    - mentions_member: Filter by mentioned member (paramType: STRING, optional)
    - page: Page number (paramType: STRING, optional) (e.g., "1")
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {}
    
    if query:
        params["query"] = query
    if sort_by:
        params["sort_by"] = sort_by
    if from_member:
        params["from_member"] = from_member
    if from_organization:
        params["from_organization"] = from_organization
    if author_job_title:
        params["author_job_title"] = author_job_title
    if author_company:
        params["author_company"] = author_company
    if content_type:
        params["content_type"] = content_type
    if mentions_organization:
        params["mentions_organization"] = mentions_organization
    if author_industry:
        params["author_industry"] = author_industry
    if mentions_member:
        params["mentions_member"] = mentions_member
    if page:
        params["page"] = page
        
    # Convert params to query string with URL encoding
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/search_posts_with_filters?{query_string}", headers=LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Search Jobs
@mcp.tool()
def search_jobs(query: str, page: str = "1", searchLocationId: str = None, experience: str = None,
               postedAgo: str = None, locationIdsList: str = None, sortBy: str = None,
               titleIdsList: str = None, workplaceType: str = None, functionIdsList: str = None,
               industryIdsList: str = None, jobType: str = None, companyIdsList: str = None,
               easyApply: str = None) -> Dict:
    """Search for jobs with filters as per linkedin

    NOTE: API doc shows this endpoint uses different parameter names than previously implemented.
    
    Get Request Parameters:
    - query: Job search keywords (paramType: STRING, required) (e.g., "software engineer")
    - page: Page number (paramType: STRING, required) (e.g., "1")
    - searchLocationId: Location ID (paramType: STRING, optional) (e.g., "Europe")
    - experience: Experience level (paramType: STRING, optional)
    - postedAgo: Filter by post date (paramType: STRING, optional)
    - locationIdsList: List of location IDs (paramType: STRING, optional)
    - sortBy: Sort results by (paramType: STRING, optional)
    - titleIdsList: List of job title IDs (paramType: STRING, optional)
    - workplaceType: Type of workplace (paramType: STRING, optional)
    - functionIdsList: List of function IDs (paramType: STRING, optional)
    - industryIdsList: List of industry IDs (paramType: STRING, optional)
    - jobType: Type of job (paramType: STRING, optional)
    - companyIdsList: List of company IDs (paramType: STRING, optional)
    - easyApply: Filter for easy apply jobs (paramType: STRING, optional)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {
        "query": query,
        "page": page
    }
    
    if searchLocationId:
        params["searchLocationId"] = searchLocationId
    if experience:
        params["experience"] = experience
    if postedAgo:
        params["postedAgo"] = postedAgo
    if locationIdsList:
        params["locationIdsList"] = locationIdsList
    if sortBy:
        params["sortBy"] = sortBy
    if titleIdsList:
        params["titleIdsList"] = titleIdsList
    if workplaceType:
        params["workplaceType"] = workplaceType
    if functionIdsList:
        params["functionIdsList"] = functionIdsList
    if industryIdsList:
        params["industryIdsList"] = industryIdsList
    if jobType:
        params["jobType"] = jobType
    if companyIdsList:
        params["companyIdsList"] = companyIdsList
    if easyApply:
        params["easyApply"] = easyApply
        
    # Convert params to query string with URL encoding
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/search_jobs?{query_string}", headers=LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Job Details
@mcp.tool()
def job_details(job_id: str) -> Dict:
    """Get detailed information about a specific job
    
    Get Request Parameters:
    - jobId: LinkedIn job ID (paramType: STRING, required) (e.g., "3862806121" - obtain from search results)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"jobId": job_id}
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/job_details?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Similar Profiles
@mcp.tool()
def similar_profiles(profileUrl: str) -> Dict:
    """Returns similar profiles to a given linkedin profile url
    
    Get Request Parameters:
    - profileUrl: LinkedIn profile URL (paramType: STRING, required) (e.g., "https://www.linkedin.com/in/williamhgates/")
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"profileUrl": profileUrl}
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/similar_profiles?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Suggestion Location
@mcp.tool()
def suggestion_location(query: str) -> Dict:
    """Suggestions per query
    
    Get Request Parameters:
    - query: Search query (paramType: STRING, required) (e.g., "California")
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"query": query}
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/suggestion_location?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Suggestion Company
@mcp.tool()
def suggestion_company(query: str) -> Dict:
    """Suggestions per query
    
    Get Request Parameters:
    - query: Search query (paramType: STRING, required) (e.g., "Google")
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"query": query}
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/suggestion_company?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Suggestion School
@mcp.tool()
def suggestion_school(query: str) -> Dict:
    """Suggestions per query
    
    Get Request Parameters:
    - query: Search query (paramType: STRING, required) (e.g., "Stanford")
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"query": query}
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/suggestion_school?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Suggestion Industry
@mcp.tool()
def suggestion_industry(query: str) -> Dict:
    """Suggestions per query
    
    Get Request Parameters:
    - query: Search query (paramType: STRING, required) (e.g., "Technology")
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"query": query}
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/suggestion_industry?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Suggestion Service Category
@mcp.tool()
def suggestion_service_catagory(query: str) -> Dict:
    """Suggestions as per query
    
    Get Request Parameters:
    - query: Search query (paramType: STRING, required) (e.g., "Consulting")
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"query": query}
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/suggestion_service_catagory?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Suggestion Person
@mcp.tool()
def suggestion_person(query: str) -> Dict:
    """Returns a list of people suggestion from linkedin.
    
    Get Request Parameters:
    - query: Search query (paramType: STRING, required) (e.g., "Bill Gates")
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"query": query}
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/suggestion_person?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Search Geo URNs
@mcp.tool()
def search_geourns(keyword: str) -> Dict:
    """Suggestions per query

    NOTE: Failed during testing when keyword contained spaces (e.g., "New York"). Needs URL encoding or API fix.
    
    Get Request Parameters:
    - keyword: Search keyword (paramType: STRING, required) (e.g., "California", avoid spaces)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {"keyword": keyword}
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/search_geourns?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Suggestion Function
@mcp.tool()
def suggestion_function(query: str = None) -> Dict:
    """Gets suggestions for Job Function
    
    Get Request Parameters:
    - query: Search query (paramType: STRING, optional) (e.g., "Engineering")
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    params = {}
    if query:
        params["query"] = query
    query_string = "&".join([f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items()])
    conn.request("GET", f"/suggestion_function?{query_string}", None, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Suggestion Company Size
@mcp.tool()
def suggestion_company_size() -> Dict:
    """Suggestions for company size filter
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    headers = LINKEDIN_HEADERS.copy()
    
    conn.request("GET", "/suggestion_company_size", headers=headers)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Suggestion Language
@mcp.tool()
def suggestion_language() -> Dict:
    """Suggestions for language filter
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    headers = LINKEDIN_HEADERS.copy()
    
    conn.request("GET", "/suggestion_language", headers=headers)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Private David
@mcp.tool()
def profiles_david(links: List[str]) -> Dict:
    """Scrape 100 profiles in a single API call

    NOTE: Marked as private/premium in documentation.
    
    Request Body Example:
    {
        "links": [
            "http://www.linkedin.com/in/luke-sharp-b3838719a",
            "http://www.linkedin.com/in/hollie-smith-96ab44b5"
        ]
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"links": links})
    conn.request("POST", "/profiles_david", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Private Skander
@mcp.tool()
def private_chtiouisk(links: List[str], count: int = 5) -> Dict:
    """This is a private endpoint for our premium user

    NOTE: Marked as private/premium in documentation.
    
    Request Body Example:
    {
        "links": [
            "http://www.linkedin.com/in/luke-sharp-b3838719a",
            "http://www.linkedin.com/in/rodneydbainjr"
        ],
        "count": 5
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"links": links, "count": count})
    conn.request("POST", "/private_chtiouisk", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Person Data With Open To Work Flag
@mcp.tool()
def person_data_with_open_to_work_flag(link: str) -> Dict:
    """Scrapes person data with open to work flag
    
    Request Body Example:
    {
        "link": "https://www.linkedin.com/in/ingmar-klein"
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"link": link})
    conn.request("POST", "/person_data_with_open_to_work_flag", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Private Search Posts with Filters
@mcp.tool()
def original_search_posts_with_filters(query: str = None, author_company: str = None, author_job_title: str = None, 
                                author_industry: str = None, from_member: str = None, from_organization: str = None, 
                                mentions_member: str = None, mentions_organization: str = None, content_type: str = None, 
                                sort_by: str = None, page: str = None) -> Dict:
    """Search for posts as per linkedin using all the available filters

    NOTE: Marked as private/premium in documentation.
    
    Get Request Parameters:
    - query: Search query (paramType: STRING, optional)
    - author_company: Filter by author's company (paramType: STRING, optional)
    - author_job_title: Filter by author's job title (paramType: STRING, optional)
    - author_industry: Filter by author's industry (paramType: STRING, optional)
    - from_member: Filter by member (paramType: STRING, optional)
    - from_organization: Filter by organization (paramType: STRING, optional)
    - mentions_member: Filter by mentioned member (paramType: STRING, optional)
    - mentions_organization: Filter by mentioned organization (paramType: STRING, optional)
    - content_type: Filter by content type (paramType: STRING, optional)
    - sort_by: Sort results by (paramType: STRING, optional)
    - page: Page number (paramType: STRING, optional)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    headers = LINKEDIN_HEADERS.copy()
    
    # Build query parameters
    params_list = []
    if query:
        params_list.append(f"query={urllib.parse.quote(str(query))}")
    if author_company:
        params_list.append(f"author_company={urllib.parse.quote(str(author_company))}")
    if author_job_title:
        params_list.append(f"author_job_title={urllib.parse.quote(str(author_job_title))}")
    if author_industry:
        params_list.append(f"author_industry={urllib.parse.quote(str(author_industry))}")
    if from_member:
        params_list.append(f"from_member={urllib.parse.quote(str(from_member))}")
    if from_organization:
        params_list.append(f"from_organization={urllib.parse.quote(str(from_organization))}")
    if mentions_member:
        params_list.append(f"mentions_member={urllib.parse.quote(str(mentions_member))}")
    if mentions_organization:
        params_list.append(f"mentions_organization={urllib.parse.quote(str(mentions_organization))}")
    if content_type:
        params_list.append(f"content_type={urllib.parse.quote(str(content_type))}")
    if sort_by:
        params_list.append(f"sort_by={urllib.parse.quote(str(sort_by))}")
    if page:
        params_list.append(f"page={urllib.parse.quote(str(page))}")
    
    params = "&".join(params_list)
    if params:
        params = "?" + params
    
    conn.request("GET", f"/original_search_posts_with_filters{params}", headers=headers)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Private Company Insights 2
@mcp.tool()
def private_company_insights_2(link: str) -> Dict:
    """Private endpoint to scrapes company insights

    NOTE: Marked as private/premium in documentation.
    
    Get Request Parameters:
    - link: Company LinkedIn URL (paramType: STRING, required)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    headers = LINKEDIN_HEADERS.copy()
    
    # Build query parameters
    params = f"?link={urllib.parse.quote(str(link))}"
    conn.request("GET", f"/private_company_insights_2{params}", headers=headers)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Post Reposts Original
@mcp.tool()
def post_reposts_original(repostsUrn: str, page: str) -> Dict:
    """Private

    NOTE: Marked as private/premium in documentation.
    
    Get Request Parameters:
    - repostsUrn: URN for the post reposts (paramType: STRING, required)
    - page: Page number (paramType: STRING, required)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    headers = LINKEDIN_HEADERS.copy()
    
    # Build query parameters
    params = f"?repostsUrn={repostsUrn}&page={page}"
    conn.request("GET", f"/post_reposts_original{params}", headers=headers)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Profile Updates Original
@mcp.tool()
def profile_updates_original(profile_url: str, page: str) -> Dict:
    """Private

    NOTE: Marked as private/premium in documentation.
    
    Get Request Parameters:
    - profile_url: LinkedIn profile URL (paramType: STRING, required)
    - page: Page number (paramType: STRING, required)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    headers = LINKEDIN_HEADERS.copy()
    
    # Build query parameters
    params = f"?profile_url={profile_url}&page={page}"
    conn.request("GET", f"/profile_updates_original{params}", headers=headers)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Company Updates Original
@mcp.tool()
def company_updates_original(company_url: str, page: int) -> Dict:
    """Original data

    NOTE: Marked as private/premium in documentation.
    
    Get Request Parameters:
    - company_url: LinkedIn company URL (paramType: STRING, required)
    - page: Page number (paramType: STRING, required)
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    headers = LINKEDIN_HEADERS.copy()
    
    # Build query parameters
    params = f"?company_url={company_url}&page={page}"
    conn.request("GET", f"/company_updates_original{params}", headers=headers)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: All posts from a profile
@mcp.tool()
def profile_posts_all(link: str) -> Dict:
    """This endpoint scrapes all posts posted by a user at linkedin.com since joined.

    NOTE: Marked as private/premium in documentation.
    
    Request Body Example:
    {
        "link": "https://www.linkedin.com/in/ingmar-klein"
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"link": link})
    conn.request("POST", "/profile_posts_all", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Person Data With All Experiences
@mcp.tool()
def person_data_with_experiences(link: str) -> Dict:
    """Scrapes all linkedin profile data alongwith all the experiences.
    
    Request Body Example:
    {
        "link": "https://www.linkedin.com/in/ingmar-klein"
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"link": link})
    conn.request("POST", "/person_data_with_experiences", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Person Data With All Languages
@mcp.tool()
def person_data_with_languages(link: str) -> Dict:
    """Scrapers person data with all languages data
    
    Request Body Example:
    {
        "link": "https://www.linkedin.com/in/matiss-brunavs/"
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"link": link})
    conn.request("POST", "/person_data_with_languages", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

# Tool: Person Data With All Educations
@mcp.tool()
def person_data_with_educations(link: str) -> Dict:
    """Scrapers person data along with all the educations data.
    
    Request Body Example:
    {
        "link": "https://www.linkedin.com/in/ingmar-klein"
    }
    """
    conn = http.client.HTTPSConnection(LINKEDIN_API_HOST)
    payload = json.dumps({"link": link})
    conn.request("POST", "/person_data_with_educations", payload, LINKEDIN_HEADERS)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data.decode("utf-8"))

if __name__ == "__main__":
    mcp.run()
