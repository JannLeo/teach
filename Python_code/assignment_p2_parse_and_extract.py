import sys

def init_data_structures(treewidth_param):
   return {
       'paren_start_indices': [],
       'vertex_counter': treewidth_param + 1,
       'global_vertex_count_after_subparse': 0,
       'subparse_vertex_counter_list': [],
       'subparse_current_vertex_count_list': [],
       'subparse_adjacency_lists': [],
       'subparse_boundary_maps': [],
       'adjacency_list': [],
       'boundary_map': [],
       'temp_adjacency_list': [],
       'temp_boundary_map': [],
       'last_processed_paren_info': [],
       'is_initial_parse_context': True
   }

def ensure_list_size(list_to_check, min_size, fill_value=None):
   while len(list_to_check) < min_size:
       list_to_check.append(fill_value)
   return list_to_check

def ensure_subparse_lists_size(data, subparse_index):
   ensure_list_size(data['subparse_adjacency_lists'], subparse_index + 1, [])
   ensure_list_size(data['subparse_boundary_maps'], subparse_index + 1, [])
   ensure_list_size(data['subparse_vertex_counter_list'], subparse_index + 1, 0)
   ensure_list_size(data['subparse_current_vertex_count_list'], subparse_index + 1, 0)

def ensure_adjacency_list_size(adjacency_list, size):
   while len(adjacency_list) < size:
       adjacency_list.append([])
   return adjacency_list

def init_subparse_structure(treewidth_param):
   adj_list = [[] for _ in range(treewidth_param + 1)]
   boundary_map = list(range(treewidth_param + 1))
   return adj_list, boundary_map

def parse_substring_edge(adj_list, boundary_map, op_i, op_j):
   u_idx = boundary_map[op_i]
   v_idx = boundary_map[op_j]
   
   max_idx = max(u_idx, v_idx)
   while len(adj_list) <= max_idx:
       adj_list.append([])
   
   if v_idx not in adj_list[u_idx]:
       adj_list[u_idx].append(v_idx)
   if u_idx not in adj_list[v_idx]:
       adj_list[v_idx].append(u_idx)

def parse_substring_vertex(data, adj_list, boundary_map, op_i, subparse_index=None):
   adj_list.append([])
   boundary_map[op_i] = len(adj_list) - 1
   data['vertex_counter'] += 1
   
   if subparse_index is not None:
       data['subparse_vertex_counter_list'][subparse_index] += 1

def create_vertex_mapping(source_map, target_map, source_adj_list, target_next_idx, treewidth_param):
   vertex_mapping = {}
   
   for src_idx in range(len(source_adj_list)):
       try:
           boundary_label = source_map.index(src_idx)
           vertex_mapping[src_idx] = target_map[boundary_label]
       except ValueError:
           vertex_mapping[src_idx] = target_next_idx
           target_next_idx += 1
           
   return vertex_mapping, target_next_idx

def merge_adjacency_lists(source_adj_list, target_adj_list, vertex_mapping):
   for src_idx_a in range(len(source_adj_list)):
       mapped_idx_a = vertex_mapping[src_idx_a]
       
       while mapped_idx_a >= len(target_adj_list):
           target_adj_list.append([])
       
       mapped_neighbors = [vertex_mapping[b] for b in source_adj_list[src_idx_a]]
       target_adj_list[mapped_idx_a] = list(set(target_adj_list[mapped_idx_a] + mapped_neighbors))

def print_result(vertex_counter, adjacency_list):
   print(vertex_counter)
   
   while len(adjacency_list) < vertex_counter:
       adjacency_list.append([])
   
   for vertex_idx in range(vertex_counter):
       if vertex_idx < len(adjacency_list):
           neighbors_list = sorted(adjacency_list[vertex_idx])
           if not neighbors_list:
               print("")
           else:
               print(" ".join(map(str, neighbors_list)))
       

def parse_substring(input_line, start_index, end_index, treewidth_param, adj_list, boundary_map, data, subparse_index=None):
   subparse_char_index = start_index + 1
   while subparse_char_index < end_index:
       sub_char = input_line[subparse_char_index]
       
       if (sub_char.isdigit() and subparse_char_index + 1 < end_index and 
           input_line[subparse_char_index+1].isdigit() and 
           input_line[subparse_char_index-1] == ' '):
           
           op_i = int(sub_char)
           op_j = int(input_line[subparse_char_index+1])
           
           if op_i <= treewidth_param and op_j <= treewidth_param and op_i > op_j:
               parse_substring_edge(adj_list, boundary_map, op_i, op_j)
               
           subparse_char_index += 1
           
       elif (sub_char.isdigit() and subparse_char_index + 1 < end_index and 
             input_line[subparse_char_index+1] == ' ' and 
             input_line[subparse_char_index-1] == ' '):
           
           op_i = int(sub_char)
           if 0 <= op_i <= treewidth_param:
               parse_substring_vertex(data, adj_list, boundary_map, op_i, subparse_index)
               
       subparse_char_index += 1
   
   return input_line[:start_index] + ' ' * (end_index - start_index + 1) + input_line[end_index+1:]

def is_condition1(data, start_index):
   return (data['last_processed_paren_info'] and 
           len(data['paren_start_indices']) >= 2 and 
           data['last_processed_paren_info'][-1] < start_index and 
           data['last_processed_paren_info'][-1] < data['paren_start_indices'][-1])

def is_condition2(data, start_index):
   return (len(data['last_processed_paren_info']) >= 2 and 
           len(data['paren_start_indices']) >= 2 and 
           data['last_processed_paren_info'][-1] < start_index and 
           data['last_processed_paren_info'][-1] > data['paren_start_indices'][-1])

def is_condition3(data, start_index, end_index):
   return (len(data['last_processed_paren_info']) >= 2 and 
           data['last_processed_paren_info'][-1] > start_index and 
           data['last_processed_paren_info'][-1] < end_index)

def is_condition4(data, start_index, end_index):
   return (data['last_processed_paren_info'] and 
           data['last_processed_paren_info'][-1] > start_index and 
           data['last_processed_paren_info'][-1] < end_index)

def should_merge_upward(data):
   return (len(data['last_processed_paren_info']) >= 2 and 
           data['paren_start_indices'] and 
           data['last_processed_paren_info'][-2] > data['paren_start_indices'][-1])

def ensure_main_graph_initialized(data, treewidth_param):
   if not data['adjacency_list']:
       data['boundary_map'] = list(range(treewidth_param + 1))
       data['adjacency_list'] = [[] for _ in range(treewidth_param + 1)]
       data['global_vertex_count_after_subparse'] = treewidth_param + 1

def parse_and_extract_graph():
   should_continue_processing = True
   
   while should_continue_processing:
       try:
           input_line = input()
           
           if not input_line or input_line[0] == "0":
               should_continue_processing = False
               continue
               
           treewidth_param = int(input_line[0])
           
           data = init_data_structures(treewidth_param)
           
           current_char_index = 0
           while current_char_index < len(input_line):
               char = input_line[current_char_index]
               
               if char == '(':
                   data['paren_start_indices'].append(current_char_index)
               elif char == ')':
                   if not data['paren_start_indices']:
                       break
                       
                   start_index = data['paren_start_indices'].pop()
                   end_index = current_char_index

                   if is_condition1(data, start_index):
                       subparse_index = len(data['last_processed_paren_info']) - 1
                       ensure_subparse_lists_size(data, subparse_index)
                       
                       data['subparse_vertex_counter_list'][subparse_index] = treewidth_param + 1
                       current_subparse_adj, current_subparse_map = init_subparse_structure(treewidth_param)
                       
                       input_line = parse_substring(
                           input_line, start_index, end_index, treewidth_param, 
                           current_subparse_adj, current_subparse_map, data, subparse_index
                       )
                       
                       data['subparse_adjacency_lists'][subparse_index] = current_subparse_adj
                       data['subparse_boundary_maps'][subparse_index] = current_subparse_map
                       data['subparse_current_vertex_count_list'][subparse_index] = data['subparse_vertex_counter_list'][subparse_index]
                       
                       data['last_processed_paren_info'].append(start_index + 1)
                       current_char_index = start_index - 1
                   
                   elif is_condition2(data, start_index):
                       subparse_index = len(data['last_processed_paren_info']) - 2
                       
                       data['temp_boundary_map'] = list(range(treewidth_param + 1))
                       data['temp_adjacency_list'] = [[] for _ in range(treewidth_param + 1)]
                       
                       input_line = parse_substring(
                           input_line, start_index, end_index, treewidth_param, 
                           data['temp_adjacency_list'], data['temp_boundary_map'], data
                       )
                       
                       stored_subparse_map = data['subparse_boundary_maps'][subparse_index]
                       stored_subparse_adj = data['subparse_adjacency_lists'][subparse_index]
                       stored_subparse_next_available_index = data['subparse_current_vertex_count_list'][subparse_index]
                       
                       vertex_mapping, new_next_idx = create_vertex_mapping(
                           data['temp_boundary_map'], stored_subparse_map, 
                           data['temp_adjacency_list'], stored_subparse_next_available_index,
                           treewidth_param
                       )
                       data['subparse_current_vertex_count_list'][subparse_index] = new_next_idx
                       merge_adjacency_lists(data['temp_adjacency_list'], stored_subparse_adj, vertex_mapping)
                       
                       data['temp_adjacency_list'] = []
                       data['temp_boundary_map'] = []
                       current_char_index = start_index - 1
                   
                   elif is_condition3(data, start_index, end_index):
                       subparse_index = len(data['last_processed_paren_info']) - 2
                       ensure_subparse_lists_size(data, subparse_index)
                       
                       if not data['subparse_boundary_maps'][subparse_index]:
                           data['subparse_boundary_maps'][subparse_index] = list(range(treewidth_param + 1))
                           data['subparse_adjacency_lists'][subparse_index] = [[] for _ in range(treewidth_param + 1)]
                           data['subparse_vertex_counter_list'][subparse_index] = treewidth_param + 1
                           data['subparse_current_vertex_count_list'][subparse_index] = treewidth_param + 1
                       
                       target_adj = data['subparse_adjacency_lists'][subparse_index]
                       target_map = data['subparse_boundary_maps'][subparse_index]
                       
                       input_line = parse_substring(
                           input_line, start_index, end_index, treewidth_param, 
                           target_adj, target_map, data, subparse_index
                       )
                       
                       current_char_index = start_index - 1
                       
                       if should_merge_upward(data):
                           if len(data['last_processed_paren_info']) == 2:
                               source_adj = data['subparse_adjacency_lists'][subparse_index]
                               source_map = data['subparse_boundary_maps'][subparse_index]
                               
                               ensure_main_graph_initialized(data, treewidth_param)
                               
                               vertex_mapping, new_global_idx = create_vertex_mapping(
                                   source_map, data['boundary_map'], 
                                   source_adj, data['global_vertex_count_after_subparse'],
                                   treewidth_param
                               )
                               data['global_vertex_count_after_subparse'] = new_global_idx
                               merge_adjacency_lists(source_adj, data['adjacency_list'], vertex_mapping)
                               
                               data['last_processed_paren_info'].pop()
                               
                           else:
                               parent_subparse_index = subparse_index - 1
                               source_adj = data['subparse_adjacency_lists'][subparse_index]
                               source_map = data['subparse_boundary_maps'][subparse_index]
                               target_adj = data['subparse_adjacency_lists'][parent_subparse_index]
                               target_map = data['subparse_boundary_maps'][parent_subparse_index]
                               target_next_idx = data['subparse_current_vertex_count_list'][parent_subparse_index]
                               
                               vertex_mapping, new_target_idx = create_vertex_mapping(
                                   source_map, target_map,
                                   source_adj, target_next_idx,
                                   treewidth_param
                               )
                               data['subparse_current_vertex_count_list'][parent_subparse_index] = new_target_idx
                               merge_adjacency_lists(source_adj, target_adj, vertex_mapping)
                               
                               data['last_processed_paren_info'].pop()
                   
                   elif is_condition4(data, start_index, end_index):
                       ensure_main_graph_initialized(data, treewidth_param)
                       
                       input_line = parse_substring(
                           input_line, start_index, end_index, treewidth_param, 
                           data['adjacency_list'], data['boundary_map'], data
                       )
                       
                       data['last_processed_paren_info'] = [start_index + 1]
                       current_char_index = start_index - 1
                   
                   else:
                       data['temp_boundary_map'] = list(range(treewidth_param + 1))
                       data['temp_adjacency_list'] = [[] for _ in range(treewidth_param + 1)]
                       
                       input_line = parse_substring(
                           input_line, start_index, end_index, treewidth_param, 
                           data['temp_adjacency_list'], data['temp_boundary_map'], data
                       )
                       
                       data['last_processed_paren_info'] = [start_index]
                       current_char_index = start_index - 1
                       
                       if data['is_initial_parse_context']:
                           if not data['adjacency_list']:
                               data['adjacency_list'] = data['temp_adjacency_list']
                               data['boundary_map'] = data['temp_boundary_map']
                               data['global_vertex_count_after_subparse'] = data['vertex_counter']
                           else:
                               vertex_mapping, new_global_idx = create_vertex_mapping(
                                   data['temp_boundary_map'], data['boundary_map'], 
                                   data['temp_adjacency_list'], data['global_vertex_count_after_subparse'],
                                   treewidth_param
                               )
                               data['global_vertex_count_after_subparse'] = new_global_idx
                               merge_adjacency_lists(data['temp_adjacency_list'], data['adjacency_list'], vertex_mapping)
                           
                           data['temp_adjacency_list'] = []
                           data['temp_boundary_map'] = []

               current_char_index += 1
           
           print_result(data['vertex_counter'], data['adjacency_list'])
       except EOFError:
           break

if __name__ == "__main__":
   parse_and_extract_graph()