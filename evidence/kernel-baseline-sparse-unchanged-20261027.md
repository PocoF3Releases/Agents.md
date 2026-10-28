# Unchanged sparse error review

Reviewed HEAD [current kernel](https://github.com/PocoF3Releases/kernel_xiaomi_sm8250/commit/68fe321774661c4150b80edd93f7ddc75f32ac06) against the original baseline IDs in the [published error ledger](kernel-baseline-sparse-errors-20261027.json). All **115 unresolved error reports** are covered exactly once: **111 core and 4 driver**. Their classifications remain unresolved. No source/build/Git/device mutations or test reruns were performed.

No new verified core/net lifetime or security defect was established in this pass. This is a finite source evaluation, not a declaration that the remaining errors are safe. The already-recorded optional Slimbus context-bank allocation/free device mismatch remains an unverified optional-route limitation; no active Kona impact or refactoring request is asserted.

## task signal pid credential identity

D0070, D0075, D0079, D0080, D0131, D0135, D0136, D0153, D0199, D0200, D0245, D0246, D0259

- __exit_signal documents tasklist write lock and uses rcu_dereference_check with lockdep_tasklist_lock_is_held before locking sighand (exit.c:137-149).
- __lock_task_sighand holds RCU, obtains siglock, revalidates tsk->sighand; comments explain SLAB_TYPESAFE_BY_RCU reuse (signal.c:1347-1374).
- get_task_pid obtains a PID reference within RCU; __task_pid_nr_ns uses RCU around pid_alive and PID lookup (pid.c:414-420,468-478).
- ptrace_check_attach holds tasklist read lock and documents that only current tracer can change the relationship after validation (ptrace.c:239-260). Other reported ptrace/parent expressions compare identity rather than dereference the compared pointer.
- __put_cred asserts zero usage and detachment from current before call_rcu; commit_creds operates on current with old credentials retained during publication (cred.c:135-153,427ff). mm_update_next_owner compares mm owner to current before seeking another referenced task; forget_original_parent updates under tasklist writer contract.

**Pending:** Tasklist/ptrace ownership contracts support the observed access patterns but every exported caller and replacement path has not been exhaustively proved. Identity comparisons across sparse address domains are not evidence of a dereference fault. Raw member typing still needs deliberate API/ownership review; no blanket annotations/casts.

**Action:** No source change justified by these errors alone.

## bpf jit address arithmetic

D0306

- bpf_prog_fill_jited_linfo comments explicitly define byte-offset mapping into JIT machine code; loop uses monotonically increasing verifier line offsets and checks instruction end (core.c:175-224). Production compiler accepts the intended GNU function-address arithmetic.

**Pending:** No new write/execute/lifetime flaw established. Complete verifier-to-JIT mapping and exact sparse extension support not proved; keep unresolved rather than declare blanket checker false positive.

**Action:** No source change justified by these errors alone.

## fasync reader lifetime

D0341, D0342

- kill_fasync takes rcu_read_lock around head load and traversal; kill_fasync_rcu locks fa_lock before using fa_file (fcntl.c:983-1019). Removal queues fasync_free_rcu through call_rcu (fcntl.c:879).

**Pending:** Generic fasync field/head annotations are plain; full owner close/teardown graph is not certified. No missing reader lock or wrong grace period identified in reported traversal.

**Action:** No source change justified by these errors alone.

## generic hlist rcu helpers

D0362, D0388, D0389

- hlist_bl_first_rcu uses rcu_dereference_check with bit-lock condition and strips only LIST_BL_LOCKMASK (rculist_bl.h:21-24). seq_hlist_next_rcu explicitly documents traversal must be guarded by caller rcu_read_lock (seq_file.c:1019-1041).

**Pending:** Generic helper validity is conditional on every caller. This review did not audit all call sites; generic list pointers do not require a blanket __rcu type conversion.

**Action:** No source change justified by these errors alone.

## swapper space snapshot

D0407

- total_swapcache_pages holds RCU across nr/pointer snapshot and nrpages summation (swap_state.c:72-94). init publishes after initializing all spaces and nr; exit clears count/pointer, waits synchronize_rcu, then kvfree (623-651).

**Pending:** No release-before-grace-period fault found. Full swap slot reuse/allocator concurrency and count-value ordering not runtime tested; source documents reuse only after a grace period. Unannotated public array remains unresolved type-contract debt.

**Action:** No source change justified by these errors alone.

## session keyring identity

D0501, D0502

- lookup_user_key compares credential session keyring identity to user session keyring, then takes RCU while obtaining the key reference (process_keys.c:587-617). join_session_keyring compares a found referenced keyring against a newly prepared unpublished credential while holding key_session_mutex; commits or aborts and puts references on exits (771-838).

**Pending:** Equality checks alone do not establish UAF. Complete credential reference acquisition and user-keyring replacement contract not discharged here; no broad keyring tag changes proposed.

**Action:** No source change justified by these errors alone.

## selinux cache tail eviction

D0618, D0630

- Both insert paths execute under their cache writer spin_lock_bh (netnode.c:196-226, netport.c:144-161), append with list_add_rcu, use protected backward-tail load with explicit lockdep condition, delete_rcu and kfree_rcu (netnode.c:164-172, netport.c:112-121).

**Pending:** Reported backward-link annotation mismatch does not demonstrate missing lock. No new defect found in these eviction expressions; full policy reload/cache lifetime remains outside this finite pass.

**Action:** No source change justified by these errors alone.

## fsnotify srcu iteration

D0741, D0742, D0743

- fsnotify takes fsnotify_mark_srcu before first/next-mark traversal and releases at unified exit (fsnotify.c:359-384). Connector destroy worker detaches queued connectors, waits synchronize_srcu on same object, then frees (mark.c:164-179); other mark retirement also waits this SRCU domain.

**Pending:** Permission-event callbacks may release/reacquire SRCU via iterator helpers; a full callback graph and mark-ref lifetime audit is still pending. No observed flavor mismatch analogous to CFI; no annotation-only rewrite.

**Action:** No source change justified by these errors alone.

## module kallsyms sched lifetime

D0825, D0826, D0827

- get_ksymbol callers disable preemption; module_get_kallsym and module_kallsyms_lookup_name likewise disable preemption around RCU-sched loads (module.c:4108ff,4182-4200,4224ff). Init success publishes core kallsyms then retires init storage via call_rcu_sched, explicitly documenting preempt-disabled walks (3605-3629); failure/unload paths use synchronize_sched (2247,3640,3949,3964).

**Pending:** No wrong-grace-period issue found in this group; existing module path already matches sched readers. Complete module symbol iterator/callback exposure is not exhaustively certified; plain kallsyms field annotation remains unresolved.

**Action:** No source change justified by these errors alone.

## posix acl reference handoff

D0917, D0918

- get_cached_acl reads under RCU and pins a_refcount with refcount_inc_not_zero, retrying if final release races (posix_acl.c:37-52). Writers exchange cached pointer and release old (62-79); posix_acl_release uses kfree_rcu (posix_acl.h:53-56).

**Pending:** get_cached_acl_rcu deliberately delegates RCU protection to caller; not all filesystem call paths were audited. No new fault established; do not replace handoff with raw casts.

**Action:** No source change justified by these errors alone.

## new socket user data initialization

D1681

- Reported RCU_INIT_POINTER clears a nocopy-tagged user_data field on newly allocated clone before returning/publishing it (sock.c:1831-1847); error branches destroy clone first.

**Pending:** Multiple subsystems intentionally overlay sk_user_data; complete origin/registration semantics not audited. Initial clearing itself does not show a concurrent reader lifetime bug.

**Action:** No source change justified by these errors alone.

## udp inner offload dispatch

D1890

- skb_udp_tunnel_segment holds RCU around selecting inet/inet6_offloads, fetching ops and invoking gso callback (udp_offload.c:153-188). Callback is checked for NULL.

**Pending:** Local pointer-to-array drops annotation; producer unregister/other callers were not exhaustively reviewed. No missing reader lock found at reported load.

**Action:** No source change justified by these errors alone.

## nexthop tree update

D2028

- insert_nexthop explicitly requires rtnl_lock and uses rtnl_dereference while searching/modifying RB tree (nexthop.c:1044-1081).

**Pending:** Full netlink caller/update/put graph remains pending; no evidence justifies annotating all rbtree links or changing lock mode.

**Action:** No source change justified by these errors alone.

## nat llc and conntrack callback types

D2101, D2102, D2103, D2104, D2105, D2106, D2107, D2108, D2109, D2110, D2111, D2112, D2113, D2114, D2115, D2116, D2117, D2118, D2119, D2120, D2121, D2122, D2123, D2124, D2125, D2126, D2138, D2139, D2153, D2154, D2172, D2173, D2174, D2175, D2176, D2177, D2178, D2179, D2180, D2181, D2182, D2183, D2184, D2185, D2186, D2187, D2188, D2189, D2192, D2193, D2194, D2195, D2198, D2200, D2201, D2202, D2203, D2204, D2205, D2206, D2207

- NAT module init stores static callbacks; unload clears hooks then synchronize_rcu (amanda/ftp/irc/tftp; nf_nat_h323.c:613-624; nf_nat_pptp.c:317-321). nf_hook and nf_hook_slow provide/document packet-dispatch RCU; nf_conntrack_helper.c:382 documents this inherited reader context.
- ip_ct_attach reader explicitly takes RCU; conntrack cleanup clears hook before network-namespace cleanup grace periods. Existing rejected paired annotation experiment removed errors but introduced function noderef-modifier warnings; do not repeat or apply.
- LLC SAP lookup pins a reference, initializes callback before publication, invokes then puts SAP; receive dispatch holds network RCU (llc_core.c:70-106, llc_input.c:187-213, dev.c:5215-5217,5400-5414).

**Pending:** Function-pointer annotation placement and old RCU macro typeof/noderef compatibility remain unresolved. Source protection evidence is not exhaustive module-unload/expectation/timer callback proof. No report is dismissed as inherited or marked checker-false; no added force casts.

**Action:** No source change justified by these errors alone.

## nfnetlink socket shutdown

D2141

- Per-net init publishes socket; exit clears net->nfnl, waits synchronize_net, then releases saved socket (nfnetlink.c:590-617).

**Pending:** No release-before-clear/grace issue found. Other users and public field type consistency remain unresolved.

**Action:** No source change justified by these errors alone.

## conntrack helper identity

D2168

- ctnetlink_change_helper enters RCU before finding helper and comparison/update callback, exits afterward (nf_conntrack_netlink.c:1634-1655). Comparison does not dereference help->helper; actual helper->from_nlattr uses the RCU-protected lookup result.

**Pending:** Conntrack mutation serialization and callback lifetime beyond this branch remain pending. Address-domain comparison is not sufficient to prove runtime misuse.

**Action:** No source change justified by these errors alone.

## nat protocol array initialization

D2199

- nf_nat_l4proto_register allocates new array under nf_nat_proto_mutex, initializes entries to static unknown proto before publication, executes smp_wmb, publishes, then registers requested proto (nf_nat_core.c:690-727).

**Pending:** New-array initialization has no concurrent reader. Complete protocol removal/memory-order graph remains pending; plain array element type mismatch not fixed in isolation.

**Action:** No source change justified by these errors alone.

## conncount rcu tree

D2208, D2209, D2210

- count_tree performs RCU loads then list_lock-protected count updates; insertion holds hashed spin_lock_bh and uses rb_link_node_rcu (nf_conncount.c:468-537). tree_nodes_free queues node reclaim via call_rcu at380. GC worker uses RCU for scan and hash lock for destructive pass (548-591). Only external count_skb caller found is xt_connlimit match, under netfilter dispatch RCU.

**Pending:** Lockless rb rotations/GC walks, count estimates, destroy entrypoint quiescence and all expression shutdown paths remain pending. No concrete freed-node access was established; RCU API error alone is not a lifetime verdict.

**Action:** No source change justified by these errors alone.

## qrtr locked radix slot identity

D2271, D2274

- Release callback is reached through kref/rwsem release contract and unlocks qrtr_node_lock writer after radix deletion (qrtr.c:336-359). endpoint_unregister holds qrtr_node_lock reader across slot traversal and comparison (1296-1326). Both reports compare node identity to typed radix slot without dereferencing slot target.

**Pending:** Other QRTR tx-flow lists and asynchronous endpoint lifetime are not certified. Do not blanket cast radix slot types or replace reference/lock ownership.

**Action:** No source change justified by these errors alone.

## traffic control chain updates

D2283, D2284

- tcf_chain_tp_remove compares head identity and uses rtnl_dereference for saved next; find walks chain via rtnl_dereference under rtnetlink mutation contract (cls_api.c:1054-1105).

**Pending:** Every offload/caller lock state and tcf proto retirement remains pending; report does not justify changing RCU publication or lifetime.

**Action:** No source change justified by these errors alone.

## xfrm socket and afinfo lifetime

D2584, D2585, D2592, D2593, D2594

- Inline listener probes explicitly hold RCU (xfrm.h:1829-1851). xfrm_nlmsg_multicast documents caller RCU; socket exit clears pointer, synchronize_net, releases stash (xfrm_user.c:1103-1109,3458-3465). afinfo unregister serializes equality check/clear with spin_lock_bh, then synchronize_rcu; getter takes RCU before dereference (xfrm_input.c:68-95).

**Pending:** All multicast callers and successful afinfo getter unlock sites are not exhaustively audited. No release-before-grace or missing-lock defect found at reported sites; do not claim global XFRM safety.

**Action:** No source change justified by these errors alone.

## slimbus mixed dma mmio

D1712

- mem->base is either dev->lpass.base IO mapping or dma_alloc_coherent RAM; each producer has different clearing/access API (slim-msm.c:164-188). Consumers share the unqualified descriptor, so conditional qualifier conflict is genuine origin ambiguity, not solved by one annotation.
- Additional existing conditional DMA API mismatch: coherent allocation selects cb_dev when present (168-174), but free always uses dev->dev (194-199).

**Pending:** Parent/driver receipt found no active Kona LPASS/context-bank DT path. Bounds, descriptor origin and platform route remain unresolved. No target corruption proved.

**Action:** Record as an unverified optional-backend limitation only. No active Kona impact established and no optional-backend refactor or source change proposed.

## smem public pointer offset

D1731, D1732, D1733

- qcom_smem_virt_to_phys accepts public ordinary void pointer, range-checks against IO-mapped partition/region bases, subtracts to form offset and adds physical base (smem.c:766-817). These expressions do address arithmetic, not memory dereference.

**Pending:** Public mapping/API qualifier contract remains inconsistent; remote metadata bounds/trust and all consumers not audited. No wrong offset on current target or exploitable access established; blanket force casts rejected.

**Action:** No source change justified by these errors alone.

## Limits

RCU annotations are opt-in in upstream documentation; absent annotations plus deliberate API checks do not themselves prove bad lifetime. Explicit reader/update/free edges were inspected where stated. Generic helpers, exported entrypoints and callback graphs retain pending caller obligations. Existing ip_ct_attach experiment remains rejected and was not repeated. No warnings were suppressed, no blanket tags/casts proposed, and no new tests or running build outputs were touched.
